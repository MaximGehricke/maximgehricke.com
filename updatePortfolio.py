import os
import re

imagePath = "images/portfolio/"
oldProjectsImagePath = "images/oldprojects/"
projectpagesPath = "projectpages/"
libName = "portfolio_lib.txt"

path = (os.path.abspath(__file__)).replace("updatePortfolio.py", "")

def readLib(lib):
    """
    Reads in the library text file.
    Returns lists of titles, image_sources, and hrefs.
    Dynamically reads until end of file without arbitrary limits.
    """
    title = []
    imageSource = []
    href = []

    with open(lib, 'r', encoding='utf-8') as l:
        lines = l.readlines()
    
    # Process 4 lines per item: Title, Image, URL, Empty line
    i = 0
    while i < len(lines):
        t = lines[i].strip()
        if not t:
            i += 1
            continue
        
        if i + 2 < len(lines):
            title.append(t)
            imageSource.append(lines[i+1].strip())
            href.append(lines[i+2].strip())
            i += 4
        else:
            if i < len(lines):
                title.append(t)
                if i+1 < len(lines): imageSource.append(lines[i+1].strip())
                if i+2 < len(lines): href.append(lines[i+2].strip())
            break
            
    return title, imageSource, href


def replace(oldProjects=False, template=path + "portfolio_template.html", destination=path + "portfolio.html", lib=path + libName, pp_template=path + projectpagesPath + "projectpage_template.html"):
    global imagePath
    projectPages = True

    if input("Create projectpages that don't exist yet? (Enter): "):
        projectPages = False

    if oldProjects:
        template = template.replace("portfolio", "oldprojects")
        destination = destination.replace("portfolio", "oldprojects")
        lib = lib.replace("portfolio", "oldprojects")
        imagePath = oldProjectsImagePath

    title, imageSource, href = readLib(lib)

    with open(template, 'r', encoding='utf-8') as t:
        templateContent = t.read()

    # Generate Portfolio HTML
    generated_html = ""
    for i in range(len(title)):
        img_src = imagePath + imageSource[i]
        item_href = href[i]
        item_title = title[i]
        
        target = '_blank' if item_href.startswith('http') else ''
        target_attr = f' target="{target}"' if target else ''

        item_html = f"""\t\t\t\t<div class="portfolio-item">
\t\t\t\t\t<div class="portfolioelement">
\t\t\t\t\t\t<a href="{item_href}" title="{item_title}"{target_attr}>
\t\t\t\t\t\t<img src="{img_src}" class="portfolioelement" alt="{item_title}"></a>
\t\t\t\t\t\t<p class="font1 portfolio-item-label">{item_title}</p>
\t\t\t\t\t</div>
\t\t\t\t</div>\n"""
        generated_html += item_html

    # Replace the marker
    pattern = r'(<!-- PORTFOLIO_ITEMS -->\n).*?(<!-- END_PORTFOLIO_ITEMS -->)'
    
    # Ensure END_PORTFOLIO_ITEMS exists in template if not already present
    if "<!-- PORTFOLIO_ITEMS -->" in templateContent and "<!-- END_PORTFOLIO_ITEMS -->" not in templateContent:
        templateContent = templateContent.replace("<!-- PORTFOLIO_ITEMS -->", "<!-- PORTFOLIO_ITEMS -->\n<!-- END_PORTFOLIO_ITEMS -->")

    templateContent = re.sub(pattern, r'\1' + generated_html + r'\2', templateContent, flags=re.DOTALL)

    with open(destination, "w", encoding='utf-8') as d:
        d.write(templateContent)

    # Create not yet existing project pages
    if projectPages:
        for pp, t in zip(href, title):
            if projectpagesPath in pp:
                newHtml = path + pp.replace("../", "")
                # check if exists
                if not os.path.exists(newHtml):
                    with open(pp_template, 'r', encoding='utf-8') as src, open(newHtml, 'w', encoding='utf-8') as dst:
                        template_html = src.read()
                        print(f"Creating project page for: {t} at {pp}")
                        template_html = template_html.replace("ProjectTitle", t)
                        dst.write(template_html)


if __name__ == "__main__":
    while True:
        print("update portfolio? (Enter) Or update old projects (o) Or open files? (f)")
        userInput = input()
        if "o" in userInput:
            # update old projects
            replace(oldProjects=True)
            print("Updated oldprojects.html!")
        elif "f" in userInput:
            # open the files
            os.startfile("oldprojects_lib.txt")
            os.startfile("portfolio_lib.txt")
            os.startfile(os.path.dirname(os.path.abspath(__file__)) + "/images")
        else:
            # update portfolio
            replace()
            print("Updated portfolio.html!")