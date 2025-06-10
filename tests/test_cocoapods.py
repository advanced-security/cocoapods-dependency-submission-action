import unittest

from ghastoolkit import Dependencies
from cpdsa.cocoapods import createPod, parsePod


class TestCocoaPods(unittest.TestCase):
    def test_parse_pod(self):
        data = "YogaKit (1.0.0)"
        deps = createPod(Dependencies(), data)

        self.assertEqual(len(deps), 1)
        dep = deps.find("YogaKit")
        self.assertEqual(dep.name, "YogaKit")
        self.assertEqual(dep.version, "1.0.0")

    def test_parse_pods(self):
        data = {"YogaKit (1.18.1)": ["Yoga (~> 1.14)"]}
        deps = createPod(Dependencies(), data)

        self.assertEqual(len(deps), 2)

        dep1 = deps.find("YogaKit")
        self.assertEqual(dep1.name, "YogaKit")
        self.assertEqual(dep1.version, "1.18.1")

        dep2 = deps.find("Yoga")
        self.assertEqual(dep2.name, "Yoga")
        self.assertEqual(dep2.version, "1.14")

    def test_namespace(self):
        data = "React-Core/CoreModulesHeaders (1000.0.0)"
        dep = parsePod(data)
        self.assertEqual(dep.name, "CoreModulesHeaders")
        self.assertEqual(dep.namespace, "React-Core")
        self.assertEqual(dep.version, "1000.0.0")

    def test_no_version(self):
        data = "Flipper-Boost-iOSX"
        dep = parsePod(data)
        self.assertEqual(dep.name, "Flipper-Boost-iOSX")
        self.assertEqual(dep.version, None)

    def test_parse_equalversion(self):
        data = "RCT-Folly (= 2021.07.22.00)"
        dep = parsePod(data)
        self.assertEqual(dep.name, "RCT-Folly")
        self.assertEqual(dep.version, "2021.07.22.00")
