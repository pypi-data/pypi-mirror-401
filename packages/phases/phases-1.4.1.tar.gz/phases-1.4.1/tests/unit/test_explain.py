import unittest
from unittest.mock import MagicMock, patch

from pyPhases import Data, Project, pdict

from phases.commands.explain import Explain


class TestExplain(unittest.TestCase):
    def getDefaultConfig(self):
        return pdict(
            {
                "name": "test",
                "namespace": "testns",
                "phases": [],
                "config": {"param1": "value1", "param2": "value2"},
                "exporter": [],
                "data": [],
            }
        )

    def getDiffConfig(self):
        return pdict(
            {
                "name": "test",
                "namespace": "testns",
                "phases": [],
                "config": {"param1": "value1", "param2": "changed_value", "param3": "new_value"},
                "exporter": [],
                "data": [],
            }
        )

    def test_parseRunOptions_default(self):
        """Test that the options are parsed correctly"""
        explain = Explain({})
        
        self.assertEqual(explain.diffConfigFileName, None)

    def test_parseRunOptions_with_diff(self):
        """Test that the diff option is parsed correctly"""
        explain = Explain({})
        explain.options = {
            "<dataid>": "myData",
            "-d": "config_diff.yaml",
            "-p": None,
            "-c": None,
            "-o": None,
            "--set": None,
            "-v": False,
            "<phaseName>": None,
            "<runOptions>": None,
        }

        explain.parseRunOptions()

        self.assertEqual(explain.what, "myData")
        self.assertEqual(explain.diffConfigFileName, "config_diff.yaml")

    def test_compareDependencies_no_differences(self):
        """Test comparing dependencies with no differences"""
        explain = Explain({})

        # Mock data objects
        dataObj1 = MagicMock()
        dataObj1.getDependencyDict.return_value = {"param1": "value1", "param2": "value2"}

        dataObj2 = MagicMock()
        dataObj2.getDependencyDict.return_value = {"param1": "value1", "param2": "value2"}

        differences, deep_diff_result = explain.compareDependencies(dataObj1, dataObj2)

        self.assertEqual(differences, {})

    def test_compareDependencies_with_differences(self):
        """Test comparing dependencies with differences"""
        explain = Explain({})

        # Mock data objects
        dataObj1 = MagicMock()
        dataObj1.getDependencyDict.return_value = {"param1": "value1", "param2": "value2"}

        dataObj2 = MagicMock()
        dataObj2.getDependencyDict.return_value = {"param1": "value1", "param2": "changed_value", "param3": "new_value"}

        differences, deep_diff_result = explain.compareDependencies(dataObj1, dataObj2)

        expected = {
            "param2": {"original": "value2", "diff": "changed_value"},
            "param3": {"original": None, "diff": "new_value"}
        }

        self.assertEqual(differences, expected)

        # Check that deep_diff_result is also returned
        self.assertIn('added', deep_diff_result)
        self.assertIn('removed', deep_diff_result)
        self.assertIn('changed', deep_diff_result)
        self.assertIn('unchanged', deep_diff_result)

    @patch('phases.commands.explain.Explain.log')
    def test_explainWithDiff_data_not_found(self, mock_log):
        """Test explainWithDiff when data is not found in either project"""
        explain = Explain({})
        
        # Mock projects that don't have the data
        originalProject = MagicMock()
        originalProject.getDataFromName.side_effect = Exception("Data not found")
        
        diffProject = MagicMock()
        diffProject.getDataFromName.side_effect = Exception("Data not found")
        
        explain.explainWithDiff(originalProject, diffProject, "nonexistent")
        
        # Should log error message
        mock_log.assert_any_call("Error: Data 'nonexistent' not found in either configuration")

    @patch('phases.commands.explain.Explain.log')
    @patch('builtins.print')
    def test_explainWithDiff_with_differences(self, mock_print, mock_log):
        """Test explainWithDiff with actual differences"""
        explain = Explain({})
        
        # Mock data objects with different dependencies
        originalDataObj = MagicMock()
        originalDataObj.getDependencyDict.return_value = {"param1": "value1", "param2": "value2"}
        originalDataObj.getDataId.return_value = "value1-value2--v1"
        
        diffDataObj = MagicMock()
        diffDataObj.getDependencyDict.return_value = {"param1": "value1", "param2": "changed_value"}
        diffDataObj.getDataId.return_value = "value1-changed_value--v1"
        
        # Mock projects
        originalProject = MagicMock()
        originalProject.getDataFromName.return_value = originalDataObj
        originalProject.getPhaseForData.return_value = None
        
        diffProject = MagicMock()
        diffProject.getDataFromName.return_value = diffDataObj
        diffProject.getPhaseForData.return_value = None
        
        explain.explainWithDiff(originalProject, diffProject, "testData")
        
        # Should log differences
        mock_log.assert_any_call("Differences found in config values:")

    def test_deep_diff_primitives(self):
        """Test deep diff with primitive values"""
        explain = Explain({})

        # Test identical values
        result = explain.deep_diff("value", "value")
        self.assertEqual(result['unchanged'][''], "value")
        self.assertEqual(len(result['changed']), 0)

        # Test different values
        result = explain.deep_diff("old", "new")
        self.assertEqual(result['changed']['']['original'], "old")
        self.assertEqual(result['changed']['']['diff'], "new")

        # Test with 0 values
        result = explain.deep_diff(0, 1)
        self.assertEqual(result['changed']['']['original'], 0)
        self.assertEqual(result['changed']['']['diff'], 1)

        # Test with None values
        result = explain.deep_diff(None, "value")
        self.assertEqual(result['added'][''], "value")

        result = explain.deep_diff("value", None)
        self.assertEqual(result['removed'][''], "value")

    def test_deep_diff_dictionaries(self):
        """Test deep diff with nested dictionaries"""
        explain = Explain({})

        dict1 = {
            "a": 1,
            "b": {"nested": "value1"},
            "c": "same"
        }

        dict2 = {
            "a": 2,
            "b": {"nested": "value2", "new_nested": "added"},
            "c": "same",
            "d": "new_key"
        }

        result = explain.deep_diff(dict1, dict2)

        # Check changed values
        self.assertEqual(result['changed']['a']['original'], 1)
        self.assertEqual(result['changed']['a']['diff'], 2)
        self.assertEqual(result['changed']['b.nested']['original'], "value1")
        self.assertEqual(result['changed']['b.nested']['diff'], "value2")

        # Check added values
        self.assertEqual(result['added']['b.new_nested'], "added")
        self.assertEqual(result['added']['d'], "new_key")

        # Check unchanged values
        self.assertEqual(result['unchanged']['c'], "same")

    def test_deep_diff_lists(self):
        """Test deep diff with lists"""
        explain = Explain({})

        list1 = [1, 2, 3]
        list2 = [1, 4, 3, 5]

        result = explain.deep_diff(list1, list2)

        # Check changed values
        self.assertEqual(result['changed']['[1]']['original'], 2)
        self.assertEqual(result['changed']['[1]']['diff'], 4)

        # Check added values
        self.assertEqual(result['added']['[3]'], 5)

        # Check unchanged values
        self.assertEqual(result['unchanged']['[0]'], 1)
        self.assertEqual(result['unchanged']['[2]'], 3)

    def test_deep_diff_complex_nested(self):
        """Test deep diff with complex nested structures"""
        explain = Explain({})

        obj1 = {
            "config": {
                "params": [1, 2, {"nested": "old"}],
                "settings": {"debug": False, "level": 0}
            }
        }

        obj2 = {
            "config": {
                "params": [1, 3, {"nested": "new", "added": True}],
                "settings": {"debug": True, "level": 0, "new_setting": "value"}
            }
        }

        result = explain.deep_diff(obj1, obj2)

        # Check various changes
        self.assertEqual(result['changed']['config.params[1]']['original'], 2)
        self.assertEqual(result['changed']['config.params[1]']['diff'], 3)
        self.assertEqual(result['changed']['config.params[2].nested']['original'], "old")
        self.assertEqual(result['changed']['config.params[2].nested']['diff'], "new")
        self.assertEqual(result['changed']['config.settings.debug']['original'], False)
        self.assertEqual(result['changed']['config.settings.debug']['diff'], True)

        # Check added values
        self.assertEqual(result['added']['config.params[2].added'], True)
        self.assertEqual(result['added']['config.settings.new_setting'], "value")

        # Check unchanged values
        self.assertEqual(result['unchanged']['config.params[0]'], 1)
        self.assertEqual(result['unchanged']['config.settings.level'], 0)

    def test_deep_diff_with_zero_and_falsy_values(self):
        """Test deep diff handles 0, False, empty string correctly"""
        explain = Explain({})

        obj1 = {
            "zero": 1,
            "false": True,
            "empty": "not_empty",
            "none": "value"
        }

        obj2 = {
            "zero": 0,
            "false": False,
            "empty": "",
            "none": None
        }

        result = explain.deep_diff(obj1, obj2)

        # All should be detected as changes, not ignored
        self.assertEqual(result['changed']['zero']['original'], 1)
        self.assertEqual(result['changed']['zero']['diff'], 0)
        self.assertEqual(result['changed']['false']['original'], True)
        self.assertEqual(result['changed']['false']['diff'], False)
        self.assertEqual(result['changed']['empty']['original'], "not_empty")
        self.assertEqual(result['changed']['empty']['diff'], "")
        self.assertEqual(result['removed']['none'], "value")

    def test_format_deep_diff_output(self):
        """Test formatting of deep diff output"""
        explain = Explain({})

        diff_result = {
            'added': {'new_key': 'new_value'},
            'removed': {'old_key': 'old_value'},
            'changed': {'changed_key': {'original': 'old', 'diff': 'new'}},
            'unchanged': {'same_key': 'same_value'}
        }

        output = explain.format_deep_diff_output(diff_result)

        self.assertIn("ADDED:", output)
        self.assertIn("+ new_key: new_value", output)
        self.assertIn("REMOVED:", output)
        self.assertIn("- old_key: old_value", output)
        self.assertIn("CHANGED:", output)
        self.assertIn("~ changed_key: old -> new", output)


if __name__ == '__main__':
    unittest.main()
