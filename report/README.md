# Project Report

This report describes the steps taken for the implementation in this repository.


The report PDF document was created using the [Quarto](https://quarto.org/docs/output-formats/pdf-basics.html) technical authoring and publication system. It uses Latex under the hood.

## Quarto Environment Setup

### Quarto installation

Install quarto with tinytex as Latex distro:
```bash

# download package
wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.5.56/quarto-1.5.56-linux-amd64.deb

# install package
sudo dpkg -i quarto-1.5.56-linux-amd64.deb 

# install the tinytex distro of Latex for quarto
quarto install tinytex

```

### Working with vector images

Digital published media look better when using SVG images because they don't pixelate!. Quarto requries the following package to work correctly with SVG images.

```bash
sudo apt install librsvg2-bin
```

### Fonts

The document is renderer with the following open fonts:
- [Bitter](https://fonts.google.com/specimen/Bitter) for content and titles
- [Ubuntu Mono](https://fonts.google.com/specimen/Ubuntu+Mono) for monospace text


To install a font download it and put the directory with the `ttf` files under the `/usr/local/share/fonts` directory and then run `sudo fc-cache -fv` to update the system fonts cache.

### Vscode extention

You can work with quarto using vscode as IDE. Just install the [quarto extension](https://marketplace.visualstudio.com/items?itemName=quarto.quarto).

## Compiling the Document

Run the `render` quarto command to compile the document. 

The output format chosen will be the one defined in the `format` key of the qmd file header. In this case I have it specified as PDF.

```bash
quarto render /path/to/document/report/report.qmd
```

This can also be achieved with the "Preview" button in vscode.