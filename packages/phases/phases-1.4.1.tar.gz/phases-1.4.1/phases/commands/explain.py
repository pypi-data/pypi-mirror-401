"""
Create a new Project
"""
from phases.commands.run import Run

from pyPhases import Project


class Explain(Run):
    """create a Phase-Project"""

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self.diffConfigFileName = None

    def parseRunOptions(self):
        super().parseRunOptions()

        if "<dataid>" in self.options:
            self.what = self.options["<dataid>"]

        if self.options["-d"]:
            self.diffConfigFileName = self.options["-d"]
            self.logDebug("Set Diff Config file: %s" % (self.diffConfigFileName))

    def runProject(self, project: Project):
        if self.diffConfigFileName:
            # Load alternative configuration for comparison
            diffProject = self.createDiffProject()
            self.explainWithDiff(project, diffProject, self.what)
        else:
            self.explain(project, self.what)

    def createDiffProject(self):
        """Create a project with the alternative configuration for comparison"""
        # Save current config state
        originalConfigFileName = self.projectConfigFileName

        # Set the diff config as the main config
        self.projectConfigFileName = self.diffConfigFileName

        # Create a new config with the diff configuration
        diffConfig = self.loadConfig(self.projectFileName, root=True)

        if self.diffConfigFileName is not None:
            configFiles = self.diffConfigFileName.split(",")
            for configFile in configFiles:
                subConfig = self.loadConfig(configFile)
                diffConfig.update(subConfig)

        diffConfig["config"] = self.overwriteConfigByEnviroment(diffConfig["config"])
        diffConfig["config"] = self.overwriteConfigByEnviromentByCliParameter(diffConfig["config"])

        self.validateConfig(diffConfig)

        # Restore original config state
        self.projectConfigFileName = originalConfigFileName

        return self.createProjectFromConfig(diffConfig)

    def deep_diff(self, obj1, obj2, path=""):
        """
        Perform deep comparison of two objects (dicts, lists, or primitives).
        Returns a dictionary with 'added', 'removed', 'changed', and 'unchanged' keys.
        """
        result = {
            'added': {},
            'removed': {},
            'changed': {},
            'unchanged': {}
        }

        # Handle None cases
        if obj1 is None and obj2 is None:
            return result
        elif obj1 is None:
            result['added'][path] = obj2
            return result
        elif obj2 is None:
            result['removed'][path] = obj1
            return result

        # Handle different types
        if not isinstance(obj1, type(obj2)) and not isinstance(obj2, type(obj1)):
            result['changed'][path] = {'original': obj1, 'diff': obj2}
            return result

        # Handle dictionaries
        if isinstance(obj1, dict) and isinstance(obj2, dict):
            all_keys = set(obj1.keys()) | set(obj2.keys())

            for key in all_keys:
                current_path = f"{path}.{key}" if path else str(key)

                if key not in obj1:
                    result['added'][current_path] = obj2[key]
                elif key not in obj2:
                    result['removed'][current_path] = obj1[key]
                else:
                    # Recursively compare nested values
                    nested_diff = self.deep_diff(obj1[key], obj2[key], current_path)

                    # Merge nested results
                    for diff_type in ['added', 'removed', 'changed', 'unchanged']:
                        result[diff_type].update(nested_diff[diff_type])

        # Handle lists
        elif isinstance(obj1, list) and isinstance(obj2, list):
            max_len = max(len(obj1), len(obj2))

            for i in range(max_len):
                current_path = f"{path}[{i}]" if path else f"[{i}]"

                if i >= len(obj1):
                    result['added'][current_path] = obj2[i]
                elif i >= len(obj2):
                    result['removed'][current_path] = obj1[i]
                else:
                    # Recursively compare list items
                    nested_diff = self.deep_diff(obj1[i], obj2[i], current_path)

                    # Merge nested results
                    for diff_type in ['added', 'removed', 'changed', 'unchanged']:
                        result[diff_type].update(nested_diff[diff_type])

        # Handle primitive values
        else:
            if obj1 == obj2:
                result['unchanged'][path] = obj1
            else:
                result['changed'][path] = {'original': obj1, 'diff': obj2}

        return result

    def format_deep_diff_output(self, diff_result):
        """Format the deep diff result for human-readable output"""
        output_lines = []

        if diff_result['added']:
            output_lines.append("  ADDED:")
            for path, value in diff_result['added'].items():
                output_lines.append(f"    + {path}: {value}")

        if diff_result['removed']:
            output_lines.append("  REMOVED:")
            for path, value in diff_result['removed'].items():
                output_lines.append(f"    - {path}: {value}")

        if diff_result['changed']:
            output_lines.append("  CHANGED:")
            for path, change in diff_result['changed'].items():
                output_lines.append(f"    ~ {path}: {change['original']} -> {change['diff']}")

        return "\n".join(output_lines) if output_lines else "  No differences found"

    def compareDependencies(self, dataObj1, dataObj2):
        """Compare dependency dictionaries between two data objects using deep diff"""
        deps1 = dataObj1.getDependencyDict()
        deps2 = dataObj2.getDependencyDict()

        # Use deep diff to compare the entire dependency dictionaries
        deep_diff_result = self.deep_diff(deps1, deps2)

        # Convert deep diff result to the expected format for backward compatibility
        differences = {}

        # Handle added items
        for path, value in deep_diff_result['added'].items():
            differences[path] = {
                'original': None,
                'diff': value
            }

        # Handle removed items
        for path, value in deep_diff_result['removed'].items():
            differences[path] = {
                'original': value,
                'diff': None
            }

        # Handle changed items
        for path, change in deep_diff_result['changed'].items():
            differences[path] = {
                'original': change['original'],
                'diff': change['diff']
            }

        return differences, deep_diff_result

    def explainWithDiff(self, originalProject: Project, diffProject: Project, what):
        """Explain with differences highlighted between two configurations"""
        self.log("Try to explain with diff: %s" % what)

        try:
            # Check if data exists in both projects
            originalDataObj = None
            diffDataObj = None

            try:
                originalDataObj = originalProject.getDataFromName(what)
            except:
                self.log(f"Warning: Data '{what}' not found in original configuration")

            try:
                diffDataObj = diffProject.getDataFromName(what)
            except:
                self.log(f"Warning: Data '{what}' not found in diff configuration")

            if originalDataObj is None and diffDataObj is None:
                self.log(f"Error: Data '{what}' not found in either configuration")
                return

            if originalDataObj is None:
                self.log(f"Data '{what}' only exists in diff configuration")
                self.explain(diffProject, what)
                return

            if diffDataObj is None:
                self.log(f"Data '{what}' only exists in original configuration")
                self.explain(originalProject, what)
                return

            # Compare dependencies
            differences, deep_diff_result = self.compareDependencies(originalDataObj, diffDataObj)

            # Show phase information
            originalPhase = originalProject.getPhaseForData(what)
            diffPhase = diffProject.getPhaseForData(what)

            if originalPhase is not None:
                self.log(f"data is generated in phase: {originalPhase.name}")

            if diffPhase is not None and diffPhase.name != originalPhase.name:
                self.log(f"diff data is generated in phase: {diffPhase.name}")

            # Show dependency comparison
            self.log("\n=== Configuration Comparison ===")

            if differences:
                self.log("Differences found in config values:")

                # Use the formatted deep diff output for better readability
                formatted_diff = self.format_deep_diff_output(deep_diff_result)
                self.log(formatted_diff)

                # Also show the traditional field-by-field comparison for backward compatibility
                self.log("\nDetailed field comparison:")
                for field, values in differences.items():
                    original_val = values['original']
                    diff_val = values['diff']
                    self.log(f"  {field}:")
                    self.log(f"    Original: {original_val}")
                    self.log(f"    Diff:     {diff_val}")
                    if original_val is None:
                        self.log("    >>> ADDED in diff config")
                    elif diff_val is None:
                        self.log("    >>> REMOVED in diff config")
                    else:
                        self.log("    >>> CHANGED in diff config")
            else:
                self.log("No differences found in dependency values")

            # Show data ID comparison
            originalDataId = originalDataObj.getDataId()
            diffDataId = diffDataObj.getDataId()

            self.log(f"\nOriginal data id: {originalDataId}")
            self.log(f"Diff data id:     {diffDataId}")

            if originalDataId != diffDataId:
                # Parse and compare data IDs
                originalId, originalVersion = originalDataId.split("--")
                diffId, diffVersion = diffDataId.split("--")

                originalValues = originalId.split("-")
                diffValues = diffId.split("-")

                fields = list(originalDataObj.getDependencyDict().keys())

                self.log("\n=== Data ID Visual Comparison ===")
                print(f"Original: {'-'.join(originalValues)}")
                print(f"Diff:     {'-'.join(diffValues)}")

                # Show visual comparison
                originalExplain = self.explainString(originalValues, fields)
                diffExplain = self.explainString(diffValues, fields)

                print("\nOriginal configuration structure:")
                print(originalExplain)
                print("\nDiff configuration structure:")
                print(diffExplain)

                # Highlight specific differences in values
                if len(originalValues) == len(diffValues):
                    print("\nValue-by-value comparison:")
                    for i, (orig, diff) in enumerate(zip(originalValues, diffValues)):
                        field_name = fields[i] if i < len(fields) else f"field_{i}"
                        if orig != diff:
                            print(f"  {field_name}: '{orig}' -> '{diff}' [CHANGED]")
                        else:
                            print(f"  {field_name}: '{orig}' [SAME]")
            else:
                self.log("Data IDs are identical - configurations produce the same result")

        except Exception as e:
            self.log(f"Error during diff comparison: {e}")
            # Fall back to regular explain
            self.explain(originalProject, what)

    def explainString(self, values, fieldNames):
        valueLength = [len(v) + 1 for v in values]
        valuePositions = [sum(valueLength[:(i)]) for i in range(len(values))]
        # valueLength[0] = 0
        linePositions = [0]
        fieldLines = [""]
        for valueIndex, valuePosition in enumerate(valuePositions):
            useLine = -1
            # find empty spots in current lines
            for index, linePosition in enumerate(linePositions):
                if valuePosition > linePosition or linePositions == 0:
                    useLine = index
                    break
                    
            # create new Line if neccessary
            if useLine == -1:
                useLine = len(fieldLines)
                fieldLines.append("")
                linePositions.append(0)
            
            # fill the line to current position
            if valuePosition > 0:
                fieldLines[useLine] += " " * (valuePosition - linePositions[useLine] - 1)
            
            name = fieldNames[valueIndex]
            if valuePosition > 0:
                name = "|" + name
                # fieldLines[useLine] += "|"
            fieldLines[useLine] += name
            # update positions
            # for i in range(useLine):

            linePositions[useLine] = len(fieldLines[useLine])
            # print("-".join(values))
            # print("\n".join(fieldLines))
        return "\n".join(fieldLines)

    def explain(self, project:Project, what):
        self.log("Try to explain: %s"%what)
        try:
            phase = project.getPhaseForData(what)
            if phase is not None:
                self.log(f"data is generated in phase: {phase.name}")

            self.log("\tit depends on following config values:")
            dataObj = project.getDataFromName(what)
            dependency_dict = dataObj.getDependencyDict()

            # Show all dependency values, including 0, False, empty strings, etc.
            for f, v in dependency_dict.items():
                self.log("%s: \t%s"%(f, v))

            self.log("data id: %s"%dataObj.getDataId())
            dataId, version = dataObj.getDataId().split("--")
            # dataId = dataObj.getDataId()
            values = dataId.split("-")
            fields = list(dependency_dict.keys())

            # Verify that all dependency values are represented in the data ID
            if len(values) != len(fields):
                self.log(f"Warning: Data ID has {len(values)} values but {len(fields)} dependencies. Some values may be missing from the ID.")
                self.log(f"Dependencies: {list(fields)}")
                self.log(f"Values in ID: {values}")

            valueString = "-".join(values)
            explainBlock = self.explainString(values, fields)
            self.log("Current value string looks like this:")
            print(valueString)
            print(explainBlock)
        except:
            pass

        if what in project.phaseMap:
            self.log(f"{what} is a phase")
