# Repo:    module-network-tree

This purpose of this code is to better understand the relationships between multiple files in a code-base.

## Description

Given the path to the directory that contains the code-base files, one can view an image of a graph network that shows the relationships between the multiple files - this includes imports and top-level packages; one can also view a text-file that contains this information.  

![Screenshot of a comment on a GitHub issue showing an image, added in the Markdown, of an Octocat smiling and raising a tentacle.](/Users/owner/Desktop/programming/module_network_tree/output/module_network_graph.png)

This code is a working roughdraft that can be further optimized for speed, clarity, utility, and length.  

## Getting Started

### Dependencies

* Python 3.9.6
* numpy == 1.26.4
* matplotlib == 3.9.4
* networkx == 3.2.1
* os (default)
* ast (default)

### Executing program

* Download this repository to your local computer
* Modify `path_to_directory` and `path_to_save_directory` in `src/example.py`
* Run `src/example.py`

## Version History

* 0.1
  * Initial Release

## License

This project is licensed under the GNU AFFERO GENERAL PUBLIC LICENSE License - see the LICENSE.md file for details