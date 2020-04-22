# Anno Tool
Small tool for calculating ratios of production chains.

- [Data folder](data) contains basic data for calculations
- [Productivities](custom_productivity.txt) Easy way to enter productivities without changes in the code

Additional way of adding a productivity is by adding the productivity directly in the code. 

## How to use
- `endproduct`: name of the resulting product you want to calculate ratios for
- `endnumber`: number of buildings you want to use for endproduct

Important: you have to enter the productivities in `times base value` rather than `percentage`. 
The result will be given in `percentage`.

### Windows
Unzip the windows release and execute the `.exe` file

[`anno_calculator_win.zip`][anno_win]

[anno_win]:https://github.com/prottmann/anno_tool/releases/download/v1.0/anno_calculator_win.zip

### Linux
Download the source code of the release or of the repository and run the code with python directly.

`python3 Gui.pyw`

`./Gui.pyw`

## Todo
- [ ] only german names for products available
- [ ] not all items are listed. 
- [x] ~~Arctic products are missing completely~~
- [ ] new world is mainly added for produciton for old world
- [ ] Ships building is missing completly
