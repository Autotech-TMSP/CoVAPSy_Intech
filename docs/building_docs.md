# How to use Markdown and MkDocs

This documentation is built using Markdown and MkDocs. This page is a guide to get you started contributing.

## What is Markdown

> Markdown is a lightweight markup language used to format text in a simple and readable way. It uses plain-text syntax to define elements like headings, lists, links, and emphasis (e.g., **bold**, *italic*). Markdown is commonly used in documentation, blogging platforms, and version control systems like GitHub because it is easy to write and converts seamlessly into HTML for web display. -ChatGPT

Markdown files are often recognizable by their `.md` and rarely `.markdown` file extensions.

## Basic Syntax

### Bold and Italics 

To make bold text, surround your text with double asterisks:
<table>
    <tr>
        <td>**This text will be bolded**</td>
        <td><b>This text will be bolded</b></td>
    </tr>
</table>

For italics, use a single asterisk:
<table>
    <tr>
        <td>*This text will be italicized*</td>
        <td><i>This text will be italicized</i></td>
    </tr>
</table>

These can be combined:
<table>
    <tr>
        <td>***This text will be bold and italic***</td>
        <td><b><i>This text will be bold and italic</i></b></td>
    </tr>
</table>

### Headings

Headings are denoted using `#` at the beginning of a line. The number of `#` determines the depth of the header:

| Input            | Render                   |
|------------------|------------------        |
| # Heading 1      | <h1> Heading 1  </h1>    |
| ## Heading 2     | <h2> Heading 2  </h2>    |
| ### Heading 3    | <h3> Heading 3  </h3>    |
| #### Heading 4   | <h4> Heading 4  </h4>    |
| ##### Heading 5  | <h5> Heading 5  </h5>    |

!!! warning 
    A space is required for a heading to work. 

    - \#Heading 1 ❌ 
    - \## Heading 1 ✔️

### Links

To add links, use the following syntax:

\[The text that will be displayed](The link to follow)

\[A link to example.org](https://example.org/)

[A link to example.org](https://example.org/)

!!! Note
    These can be used for internal links as well. For example, we can link this section with \[Links](#Links) or \[Links](/building_docs/#Links): [Links](#links).

    The second method can be generalized to reach any page or header on the website.

### Images 

The syntax to add images is almost the same as links. Alt text is the text used by accessibility readers. It should therefore be descriptive rather than a title.

\!\[Alt text](path/to/image.png)

\!\[A square version of the autotech logo. It is used as a favicon for the site](img/favicon.png)

![A square version of the autotech logo. It is used as a favicon for the site](img/favicon.png)

!!! Note
    See [Images in HTML](#images-in-html) for more fine-grain control of images.

### Code Blocks

Code blocks in Markdown can be created using triple backticks (\`\`\`). You can specify the language for syntax highlighting by adding the language name after the opening backticks. Here is an example of a code block in Python:

\`\`\`python

def hello_world():

    print("Hello, world!")

\`\`\`

```python
def hello_world():
    print("Hello, world!")
```

You can also create inline code by wrapping text in single backticks (\`). For example, \`print("Hello, world!")\` renders as `print("Hello, world!")`.

## Advanced Syntax

Markdown's strength is in the simplicity of writing, but that sometimes comes back to bite us when trying to do something a little more complicated. Luckily, most Markdown renderers accept some HTML in Markdown files. This is the case with MkDocs and GitHub. **HTML should only be used as necessary.**

### Comments

In Markdown, there is no built-in syntax for comments. However, you can use HTML comments to add notes or comments that will not be rendered in the final output. Here is an example:

```
<!-- This is a comment and will not be rendered in the final output -->
```

### Images in HTML

Images are impossible to scale or render next to text. Using the HTML `<img>` tag, it is possible to customize your image's behavior. Here is an example of an image that is scaled and displayed to the right. Keep in mind that images **can't** be rendered above the position of the `<img>` tag:

```
<img src="../img/favicon.png" alt="A square version of the autotech logo. It is used as a favicon for the site" title="A UST-10lx Lidar" width="200" align="right"/>
```

<img src="../img/favicon.png" alt="A square version of the autotech logo. It is used as a favicon for the site" title="A UST-10lx Lidar" width="200" align="right"/>

!!! warning
    Due to differences in how the HTML and Markdown are compiled, there are different paths when adding images in HTML and Markdown.

<div style="clear: both;"></div> <!-- ensure no overlap with next element -->

### Admonitions

Admonitions are a way to highlight important information in your documentation. MkDocs supports several types of admonitions, such as notes, warnings/caution, danger, and tips/hint. Here is an example of how to use them:

```
!!! note
    This is a note admonition.
```
!!! note
    This is a note admonition.

```
!!! warning
    This is a warning admonition.
```
!!! warning   
    This is a warning admonition.

## Using MkDocs

For full documentation, visit [mkdocs.org](https://www.mkdocs.org).

### Commands

* `mkdocs serve` - Start the live-reloading docs server. It should now be accessible at [127.0.0.1:8000](http://127.0.0.1:8000/) on ***your machine***.
* `mkdocs gh-deploy` - Build the documentation site on the gh-pages branch of your repository.

!!! Note
    On the [Club-INTech/CoVAPSy](https://github.com/Club-INTech/CoVAPSy) repository, `mkdocs gh-deploy` is automatically called upon push to the main branch. It can still be manually called when on another branch, but [gh-pages](https://github.com/Club-INTech/CoVAPSy/tree/gh-pages) will be overwritten by any push on main.

### Project Layout

    mkdocs.yml    ## The configuration file.
    docs/
        index.md  ## The documentation homepage.
        ...       ## Other markdown pages, images, and other files.
        img/
            favicon.png ## The icon that appears on the browser tab.
            ... other images

### Using GitHub Pages

Navigate to the repository, then to settings/pages. Using the drop-down menus, select "Deploy from branch" for source and "gh-pages" and "/root" for branch.

!!! Note
    You may have to run `mkdocs gh-deploy` for the gh-pages branch to show. See [Commands](#commands).
