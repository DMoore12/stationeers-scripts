import re

# Class representing the version of something
class Version:
    # Class variables
    major = 0
    minor = 0
    patch = 0
    proto = True

    # Constants
    EQUAL = 0
    LESS_THAN = 1
    GREATER_THAN = 2

    # ___init__()
    #
    # Creates a new version instance with the given targeted version
    #
    # Arguments:
    #   - version_major - major version
    #   - version_minor - minor version
    #   - version_patch - patch version
    #   - version_proto - boolean indicating if this is a prototype version
    def __init__(self, version_major, version_minor, version_patch, version_proto):
        self.major = version_major
        self.minor = version_minor
        self.patch = version_patch
        self.proto = version_proto

    # from_string()
    #
    # Creates a new version instance with the given targeted version
    # given a string input. Accepts strings of the form M.m.p.b where:
    #   - M is the major version
    #   - m is the minor version
    #   - p is the patch version
    #   - ".b" is optional and signifies this is a beta version
    def from_string(ver_str):
        groups = re.match(r"^(\d+)\.(\d+)\.(\d+)(\.b){,1}$", ver_str)

        # Return a default version if match fails
        if groups == None:
            return Version(0, 0, 0, 0)
        
        # Extract values
        major = int(groups[1])
        minor = int(groups[2])
        patch = int(groups[3])
        proto = True

        # Forgive me Lord, for I am lazy...
        try:
            _ = chr(groups[4])
        except:
            pass
        finally:
            proto = False

        return Version(major, minor, patch, proto)

    # islt()
    #
    # Runs the comparison self < input and returns the result
    #
    # Arguments:
    #   - v - version to compare against
    #
    # Returns:
    #   - True when version is less than the input
    def islt(self, v):
        return self.compare(v) == self.LESS_THAN
    
    # isgt()
    #
    # Runs the comparison self > input and returns the result
    #
    # Arguments:
    #   - v - version to compare against
    #
    # Returns:
    #   - True when version is greater than the input
    def isgt(self, v):
        return self.compare(v) == self.GREATER_THAN
    
    # iseq()
    #
    # Runs the comparison self == input and returns the result
    #
    # Arguments:
    #   - v - version to compare against
    #
    # Returns:
    #   - True when version is equal to the input
    def iseq(self, v):
        return self.compare(v) == self.EQUAL

    # islteq()
    #
    # Runs the comparison self <= input and returns the result
    #
    # Arguments:
    #   - v - version to compare against
    #
    # Returns:
    #   - True when version is less than or equal to the input
    def islteq(self, v):
        comp = self.compare(v)

        return comp == self.LESS_THAN or comp == self.LESS_THAN
    
    # isgteq()
    #
    # Runs the comparison self >= input and returns the result
    #
    # Arguments:
    #   - v - version to compare against
    #
    # Returns:
    #   - True when version is greater than or equal to the input
    def isgteq(self, v):
        comp = self.compare(v)

        return comp == self.LESS_THAN or comp == self.GREATER_THAN

    # compare()
    #
    # Non-static multipurpose comparison function
    #
    # Arguments:
    #   - v - input version for comparison
    #
    # Returns:
    #   - Version comparison result (less than, greater than, or equal)
    def compare(self, v):
        ret = self.EQUAL

        if self.major > v.major:
            ret = self.GREATER_THAN
        elif self.major < v.major:
            ret = self.LESS_THAN
        elif self.minor > v.minor:
            ret = self.GREATER_THAN
        elif self.minor < v.minor:
            ret = self.LESS_THAN
        elif not self.proto and v.proto:
            ret = self.GREATER_THAN

        return ret
    
    # to_string()
    #
    # Outputs the version as a user friendly string
    def to_string(self):
        ret = f"{self.major}.{self.minor}.{self.patch}"
        if self.proto:
            ret += ".b"
        return ret    

    # debug()
    #
    # Prints a debug view of the version
    def debug(self):
        print(f"{self.to_string()}")
        print(f" {self.major:3} -> major")
        print(f" {self.minor:3} -> minor")
        print(f" {self.patch:3} -> patch")
        if self.proto:
            print(f"  .b -> prototype build")

    
# Run testing
if __name__ == "__main__":
    # Create production version with string
    v1 = Version.from_string("4.5.6")
    vplo = Version.from_string("1.2.3")
    vpeq = Version.from_string("4.5.6")
    vphi = Version.from_string("7.8.9")

    # Create beta version with string
    v2 = Version.from_string("4.5.6.b")
    vblo = Version.from_string("1.2.3.b")
    vbeq = Version.from_string("4.5.6.b")
    vbhi = Version.from_string("7.8.9.b")

    # Create production version with long values
    v3 = Version.from_string("101.202.313")
    assert v3.iseq(Version(0, 0, 0, True))

    # Check equality operator
    assert v1.iseq(vpeq)
    assert not v1.iseq(v2)
    assert v2.iseq(vbeq)
    assert not v2.iseq(v1)
    assert not v1.iseq(vphi)
    assert not v2.iseq(vbhi)
    assert not v1.iseq(vplo)
    assert not v2.iseq(vblo)

    # Check less than operator
    assert not v1.islt(vpeq)
    assert not v1.islt(v2)
    assert not v2.islt(vbeq)
    assert v2.islt(v1)
    assert v1.islt(vphi)
    assert v2.islt(vbhi)
    assert not v1.islt(vplo)
    assert not v2.islt(vblo)

    # Check greater than operator
    assert not v1.isgt(vpeq)
    assert v1.isgt(v2)
    assert not v2.isgt(vbeq)
    assert not v2.isgt(v1)
    assert not v1.isgt(vphi)
    assert not v2.isgt(vbhi)
    assert v1.isgt(vplo)
    assert v2.isgt(vblo)

    # Check less than or equal to operator
    assert not v1.islteq(vpeq)
    assert not v1.islteq(v2)
    assert not v2.islteq(vbeq)
    assert v2.islteq(v1)
    assert v1.islteq(vphi)
    assert v2.islteq(vbhi)
    assert not v1.islteq(vplo)
    assert not v2.islteq(vblo)

    # Check greater than or equal to operator
    assert v1.isgteq(vpeq)
    assert v1.isgteq(v2)
    assert v2.isgteq(vbeq)
    assert not v2.isgteq(v1)
    assert not v1.isgteq(vphi)
    assert not v2.isgteq(vbhi)
    assert v1.isgteq(vplo)
    assert v2.isgteq(vblo)

    # Create an invalid version with string
    ver = Version.from_string("1.2.3.a")
    assert ver.iseq(Version(0, 0, 0, False))

    # Create an invalid version with string
    ver = Version.from_string("0,2.4,2")
    assert ver.iseq(Version(0, 0, 0, False))
