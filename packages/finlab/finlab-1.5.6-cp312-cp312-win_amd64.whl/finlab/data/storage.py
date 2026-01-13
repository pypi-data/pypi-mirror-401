import os
import pickle
import shutil
import logging
import datetime
import pandas as pd

import finlab.utils

logger = logging.getLogger(__name__)


class CacheStorage:

    def __init__(self):
        """將歷史資料儲存於快取中

          Examples:
              欲切換成以檔案方式儲存，可以用以下之方式：

              ``` py
              from finlab import data
              data.set_storage(data.CacheStorage())
              close = data.get('price:收盤價')
              ```

              可以直接調閱快取資料：

              ``` py
              close = data._storage._cache['price:收盤價']
              ```
        """

        self._cache = {}
        self._cache_time = {}
        self._cache_expiry = {}
        self._stock_names = {}

    @staticmethod
    def now():
        return datetime.datetime.now(tz=datetime.timezone.utc)

    def set_dataframe(self, name, df, expiry=None):
        self._cache[name] = df
        self._cache_time[name] = self.now()
        self._cache_expiry[name] = expiry or self.now()

    def set_stock_names(self, stock_names):
        self._stock_names = {**self._stock_names, **stock_names}

    def get_time_created(self, name):

        if name not in self._cache or name not in self._cache_time:
            return None

        return self._cache_time[name]

    def get_time_expired(self, name):

        if name in self._cache_expiry:
            return self._cache_expiry[name]

        return None
    
    def set_time_expired(self, name, expiry):
        self._cache_expiry[name] = expiry

    def get_dataframe(self, name):

        # not exists
        if name not in self._cache or name not in self._cache_time:
            return None

        return self._cache[name]

    def get_stock_names(self):
        return self._stock_names


class FileStorage:
    def __init__(self, path=None, use_cache=True):
        """將歷史資料儲存於檔案中

          Args:
                path (str): 資料儲存的路徑
                use_cache (bool): 是否額外使用快取，將資料複製一份到記憶體中。

          Examples:
              欲切換成以檔案方式儲存，可以用以下之方式：

              ``` py
              from finlab import data
              data.set_storage(data.FileStorage())
              close = data.get('price:收盤價')
              ```

              可以在本地端的 `./finlab_db/price#收盤價.pickle` 中，看到下載的資料，
              可以使用 `pickle` 調閱歷史資料：
              ``` py
              import pickle
              close = pickle.load(open('finlab_db/price#收盤價.pickle', 'rb'))
              ```
        """
        if path is None:
            path = finlab.utils.get_tmp_dir()
            
        self._path = path
        self._cache = {}
        self._stock_names = None
        self._expiry = {}
        self.use_cache = use_cache
        self._created = {}

        if not os.path.isdir(path):
            os.mkdir(path)

        f_stock_names = os.path.join(path, 'stock_names.pkl')

        if not os.path.isfile(f_stock_names):
            with open(f_stock_names, 'wb') as f:
                pickle.dump({}, f)
        else:
            with open(f_stock_names, 'rb') as f:
                self._stock_names = pickle.load(f)

        f_expiry = os.path.join(self._path, 'expiry.pkl')
        self._expiry_loaded_time = datetime.datetime.fromtimestamp(0, tz=datetime.timezone.utc)

        if os.path.isfile(f_expiry):
            with open(f_expiry, 'rb') as f:
                try:
                    self._expiry = pickle.load(f)
                    self._expiry_loaded_time = datetime.datetime.fromtimestamp(
                        os.path.getmtime(f_expiry), tz=datetime.timezone.utc)
                except:
                    self._expiry = {}
        
        if self._expiry:
            res = finlab.utils.requests.get('https://asia-east1-fdata-299302.cloudfunctions.net/data_reset_time', timeout=300)
            reset_data_time = datetime.datetime.fromtimestamp(float(res.text), tz=datetime.timezone.utc)
            for k, v in self._expiry.items():
                created = self.get_time_created(k)
                if created and created  < reset_data_time:
                    logger.info(f' set {k} time expired since the system reset time: {reset_data_time} > created time: {self.get_time_created(k)}')
                    self.set_time_expired(k, reset_data_time, save=False)

        self.save_expiry()

    def _reload_expiry_if_modified(self):
        """Reload expiry data from disk if the file has been modified by another process."""
        expiry_file = os.path.join(self._path, 'expiry.pkl')
        if not os.path.isfile(expiry_file):
            return
        
        file_mtime = datetime.datetime.fromtimestamp(
            os.path.getmtime(expiry_file), tz=datetime.timezone.utc)
        
        if file_mtime > self._expiry_loaded_time:
            with open(expiry_file, 'rb') as f:
                self._expiry = pickle.load(f)
            self._expiry_loaded_time = file_mtime
            logger.debug('Reloaded expiry data from disk (modified by another process)')

    def set_dataframe(self, name, df, expiry=None):

        file_path = os.path.join(
            self._path, name.replace(':', '#') + '.pickle')
        try:
            df.to_pickle(file_path)
        except Exception as e:
            error_msg = f'{name} save dataframe fail. Path: {file_path}. Error: {e}'
            logger.warning(error_msg)
            print(f'Warning: {error_msg}')
            print('Please check disk permission, available space, or filename encoding issues.')
            return

        # Verify the file was actually created
        if not os.path.isfile(file_path):
            error_msg = f'{name} save dataframe fail - file not created at {file_path}'
            logger.warning(error_msg)
            print(f'Warning: {error_msg}')
            return

        if self.use_cache:
            self._cache[name] = df

        self._expiry[name] = expiry or CacheStorage.now()
        self._created[name] = CacheStorage.now()
        self.save_expiry()

    def get_time_created(self, name):

        if name in self._created:
            return self._created[name]

        # check existence
        file_path = os.path.join(
            self._path, name.replace(':', '#') + '.pickle')

        if not os.path.isfile(file_path):
            return None

        return datetime.datetime.fromtimestamp(
            os.path.getmtime(file_path), tz=datetime.timezone.utc)

    def get_time_expired(self, name):
        # Reload expiry from disk if it's been modified by another process
        self._reload_expiry_if_modified()

        if name in self._expiry:
            return self._expiry[name]

        return None
    
    def set_time_expired(self, name, expiry, save=True):
        self._expiry[name] = expiry
        if save:
            self.save_expiry()

    def save_expiry(self):
        try:
            with open(os.path.join(self._path, 'expiry.pkl'), 'wb') as f:
                pickle.dump(self._expiry, f)
        except Exception as e:
            logger.warning(f' save expiry fail {e}')
            pass

    def get_dataframe(self, name):

        file_path = os.path.join(
            self._path, name.replace(':', '#') + '.pickle')

        # Check if file exists on disk
        if not os.path.isfile(file_path):
            return None

        # If we have a cached version, check if the file on disk is newer
        if name in self._cache:
            file_mtime = datetime.datetime.fromtimestamp(
                os.path.getmtime(file_path), tz=datetime.timezone.utc)
            cached_time = self._created.get(name)
            
            # If file was modified after we cached it, invalidate cache
            if cached_time and file_mtime > cached_time:
                logger.debug(f'{name} file on disk is newer than cache, reloading from disk')
                del self._cache[name]
            else:
                # Cache is still valid
                return self._cache[name]

        # Load from disk
        ret = pd.read_pickle(file_path)
        if self.use_cache:
            self._cache[name] = ret
            self._created[name] = datetime.datetime.fromtimestamp(
                os.path.getmtime(file_path), tz=datetime.timezone.utc)
        return ret

    def set_stock_names(self, stock_names):
        self._stock_names = {**self._stock_names, **stock_names}

        with open(os.path.join(self._path, 'stock_names.pkl'), 'wb') as f:
            pickle.dump(self._stock_names, f)

    def get_stock_names(self):

        if self._stock_names is not None:
            return self._stock_names

        with open(os.path.join(self._path, 'stock_names.pkl'), 'rb') as f:
            stock_names = pickle.load(f)
        self._stock_names = stock_names
        return stock_names
    
    def clear(self):
        folder_path = self._path
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

    def diagnose(self, dataset=None):
        """診斷本地儲存狀態
        
        Args:
            dataset (str, optional): 指定要檢查的資料集名稱，例如 'price:收盤價'。如果不指定，則列出所有本地資料。
        
        Examples:
            ``` py
            from finlab import data
            data._storage.diagnose()  # 列出所有本地資料
            data._storage.diagnose('price:收盤價')  # 檢查特定資料集
            ```
        """
        print(f'Storage path: {self._path}')
        print(f'Path exists: {os.path.isdir(self._path)}')
        
        if dataset:
            file_name = dataset.replace(':', '#') + '.pickle'
            file_path = os.path.join(self._path, file_name)
            print(f'\nDataset: {dataset}')
            print(f'Expected file: {file_path}')
            print(f'File exists: {os.path.isfile(file_path)}')
            if os.path.isfile(file_path):
                size_mb = os.path.getsize(file_path) / (1024 * 1024)
                mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                print(f'File size: {size_mb:.2f} MB')
                print(f'Last modified: {mtime}')
            if dataset in self._expiry:
                print(f'Expiry time: {self._expiry[dataset]}')
            else:
                print('Expiry time: Not set')
            if dataset in self._cache:
                print(f'In memory cache: Yes ({len(self._cache[dataset])} rows)')
            else:
                print('In memory cache: No')
        else:
            print('\nLocal data files:')
            pickle_files = [f for f in os.listdir(self._path) if f.endswith('.pickle') and f != 'expiry.pkl']
            if not pickle_files:
                print('  (No data files found)')
            for f in sorted(pickle_files)[:20]:  # Show first 20 files
                file_path = os.path.join(self._path, f)
                size_mb = os.path.getsize(file_path) / (1024 * 1024)
                dataset_name = f.replace('#', ':').replace('.pickle', '')
                print(f'  {dataset_name}: {size_mb:.2f} MB')
            if len(pickle_files) > 20:
                print(f'  ... and {len(pickle_files) - 20} more files')
            print(f'\nTotal: {len(pickle_files)} data files')





