from datetime import datetime
import pandas as pd
import os
import glob
import enum
import argparse

PATH = os.path.abspath(os.getcwd())
new_columns_names = {'amounts': 'amount',
                     'date': 'timestamp',
                     'date_readable': 'timestamp',
                     'type': 'transaction'}
date_fmt_readable = '%d %B %Y'
result_cols = ['timestamp', 'date_readable', 'transaction', 'amount', 'from', 'to']


class EuroEnum(enum.Enum):
    unit = 'euro'
    subunit = 'cents'


class UsdEnum(enum.Enum):
    unit = 'usd'
    subunit = 'cents'


class CurrencyEnum(enum.Enum):
    euro = EuroEnum
    usd = UsdEnum


class Aggregator:
    def __init__(self):
        self.data: pd.DataFrame = pd.DataFrame()

    def aggregate(self, path='files', file_prefix='', currency='euro'):
        """
        Method aggregates multiple csv files into one dataframe
        :param path: relative path
        :param file_prefix: files like <file_prefix>*.csv
        :param currency: transactions currency
        """
        files = self._check_files(path, file_prefix)
        # File aggregation
        modified_dfs = []
        for f in files:
            new_f = pd.read_csv(f, index_col=None, header=0)
            new_f.rename(columns=new_columns_names, inplace=True)

            modified_dfs.append(new_f)
        result = pd.concat(modified_dfs, ignore_index=True)

        # Check if there is data in files
        if result.empty:
            raise pd.errors.EmptyDataError('Files are empty. Program stops.')

        # Unify and sum columns with specified currency
        self._currency_to_amount(result, currency)

        # Timestamp modification
        result['timestamp'] = pd.to_datetime(result['timestamp'])
        result['date_readable'] = result['timestamp'].dt.strftime(date_fmt_readable)

        # Leaving only needed columns
        result = result[result_cols]
        self.data = result

    @staticmethod
    def _currency_to_amount(result_df: pd.DataFrame, currency: str):
        """
        Merges currency columns into 'amount' column
        :param result_df: resulting Dataframe
        :param currency: transactions currency
        """
        currency = CurrencyEnum[currency].value
        unit = currency.unit.value
        subunit = currency.subunit.value
        if unit in result_df.columns:
            if subunit in result_df.columns:
                result_df[subunit] = result_df[subunit].apply(lambda x: x * 0.01)
                result_df['amount'] = result_df[unit] + result_df[subunit]
            else:
                result_df['amount'] = result_df[unit]

    @staticmethod
    def _check_files(path, file_prefix) -> list:
        # Check if path exists
        if path:
            path = os.path.join(PATH, path)
            if not os.path.exists(path):
                raise FileNotFoundError(f'Wrong path {path}')
        # Check if files exist
        files = glob.glob(path + f"/{file_prefix}*.csv")
        if not files:
            raise FileNotFoundError(f"There are no files in {path}")
        if len(files) == 1:
            raise Warning(f"There is only one file in {path}. Program stops")
        return files

    def to_csv(self, filename=''):
        file = f'result{datetime.now()}.csv'
        if filename:
            file = f'{filename}.csv'

        path = os.path.join(PATH, file)

        if not self.data.empty:
            self.data.to_csv(path, index=False)
            print(f'File {file} was created in {PATH}')

    def to_xml(self):
        pass

    def to_json(self):
        pass

    def to_database(self):
        pass


if __name__ == "__main__":
    """
    Usage example:
        python csv_aggregator --files_folder files --files_prefix doc \
                              --filename result_filename
    """
    parser = argparse.ArgumentParser('')
    # TODO: any path folder
    parser.add_argument('--files_folder', default='files', type=str,
                        help='Folder in the current script location')
    parser.add_argument('--files_prefix', default='', type=str,
                        help='File_prefix in the file name like <file_prefix>*.csv')
    # TODO: currency arg
    parser.add_argument('--filename', default='', type=str,
                        help='Filename of the resulting csv. '
                             'Being saved in the current script location')
    args = parser.parse_args()
    aggregator = Aggregator()
    # Aggregates multiple csv into one Dataframe
    aggregator.aggregate(path=args.files_folder, file_prefix=args.files_prefix)
    # Saves Dataframe to resulting csv
    aggregator.to_csv(filename=args.filename)
