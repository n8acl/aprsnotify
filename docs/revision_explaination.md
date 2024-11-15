# Revisions Explaination

While updating the code to APRSNotify2, I decided to move from a dated version release (like what Home Assistant does) back to a classic Major.Minor.Build versioning format. The dated release versioning was just too confusing for me to keep track of, so I decided to change back. 

With the initial release of APRSNotify2, I also decided to revert back to starting with Version 1.0.0 since this is basically an all new program with all the changes to how the backend works.

I wanted to explain though how I will be using the versioning format, IE what will trigger a certain release.

### What will trigger a:

##### Major Version Release?
This would be any massive change to the entire code base and how the program functions. So things like moving something into a function call or moving from Apprise to something else, or major changes to the Configuration Utility or an update to the database. Anything that effects how the code runs on the backend will trigger a major release.

##### Minor Version Release?
This would be any additions or subtractions of things that doesn't effect the whole codebase. So adding a supported service or deleteing a supported service or updates to the HTML templates for the Configuration Utility would be examples of what would trigger a minor release.

##### Build Release?
This would be any bug fixes to the current codebase. If a bug or bugs are found and fixed, this would trigger a build release.
