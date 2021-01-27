import unittest
from csv_aggregator import Aggregator


class AggregatorTests(unittest.TestCase):
    # def test_files_path_doesnt_exist(self):
    #     func = Aggregator().aggregate
    #     self.assertRaises(FileNotFoundError, func, 'non_existing_folder')

    # def test_file_path_is_empty(self):
    #     func = Aggregator().aggregate
    #     self.assertRaises(FileNotFoundError, func, 'files_empty')

    def test_files_path_doesnt_exist(self):
        with self.assertRaises(FileNotFoundError) as context:
            Aggregator().aggregate(path='non_existing_folder')

        self.assertTrue('Wrong path' in str(context.exception))

    def test_file_path_is_empty(self):
        with self.assertRaises(FileNotFoundError) as context:
            Aggregator().aggregate(path='files_empty')

        self.assertTrue('There are no files' in str(context.exception))

    def test_wrong_file_prefix(self):
        with self.assertRaises(FileNotFoundError) as context:
            Aggregator().aggregate(path='files', file_prefix='doc')

        self.assertTrue('There are no files' in str(context.exception))

    def test_aggregate(self):
        aggregator = Aggregator()
        aggregator.aggregate(path='files', file_prefix='bank')
        self.assertTrue(not aggregator.data.empty)


if __name__ == '__main__':
    unittest.main()
