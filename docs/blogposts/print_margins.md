---
author: gestos
title: printmargins
categories: a4 printing mozilla firefox
date:   2019-01-09 11:59:39
---
besides the css settings, firefox will need to be adjusted if one wants to use the full area of an A4 paper sheet.  

[this](https://support.mozilla.org/en-US/questions/1061569) mozilla blog post is in the right direction, but there's a third configuration options for the margins called ***print.print_edge***, see screenshot:
<img class="full" src="/images/printmargins_firefox.png" alt="ff printmargins" />
of course, the same options shown here for ***bottom*** can be set for ***top***, ***left*** and ***right*** as well.

it seems like the relevant options are the *print.print_unwriteable_margin_* options, but that may depend on which printer you select for the print preview. There seems to be no well-structured mozilla authorized manual for this stuff and I'm too lazy to dig deeper into it right now.
setting all of those to zero will give you the full page for printing, but will also remove the page count in the formerly "unwriteable" top right corner.

[more mozilla on this topic](https://wiki.mozilla.org/Firefox:Printing_and_Page_Setup)

since I don't want the page counter removed just for the one use case that I'm fiddling with, I set the top margin to 20. The numbers seem to refer to the percenteage of an inch (see link above). I checked manually, the counter won't appear below a top margin of 20, which seems stupid, because it will respect that margin, leaving blank margin to the page edge...

Also, I changed the A4 width + height settings in my css to a value slightly lower than standard (200mm instead of 210mm width, 290mm instead of 297mm height). The "real" standard measurements seem to cause a page break even with all margins set to zero. Using these slightly smaller values however works ok.
