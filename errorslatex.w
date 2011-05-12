
\foobar

LaTeX describes what it's typesetting while it does it, and if it encounters something it doesn't understand or can't do, it will display a message saying what's wrong. It may also display warnings for less serious conditions.
s asd \foobar

''Don't panic if you see error messages'': it's very common to mistype or mis-spell commands, forget curly braces, type a forward slash instead of a backslash, or use a special character by mistake. Errors are easily spotted and easily corrected in your editor, and you can then run LaTeX again to check you have fixed everything. Some of the most common errors are described in next sections.

== Error messages ==
The format of an error message is always the same. Error messages begin with an exclamation mark at the start of the line, and give a description of the error, followed by another line starting with the number, which refers to the line-number in your document file which LaTeX was processing when the error was spotted. Here's an example, showing that the user mistyped the <tt>\tableofcontents</tt>
command:

<pre>
! Undefined control sequence.
l.6 \tableofcotnetns
</pre>

When LaTeX finds an error like this, it displays the error message and pauses. You must type one of the following letters to
continue:

{| class="wikitable"
!Key 
!Meaning
|-
|x
|Stop immediately and e'''x'''it the program.
|-
|q
|Carry on '''q'''uietly as best you can and don't bother me with any more error messages.
|-
|e
|Stop the program but re-position the text in my '''e'''ditor at the point where you found the error (This only works if you're using an editor which LaTeX can communicate with).
|-
|h
|Try to give me more '''h'''elp.
|-
|i
|(followed by a correction) means '''i'''nput the correction in place of the error and carry on (This is only a temporary fix to get the file processed. You still have to make that correction in the editor).
|-
|r
|'''r'''un in non-stop mode. Plow through any errors, unless too many pile up and it fails (100 errors).
|-
|}

Some systems (Emacs is one example) run LaTeX with a "nonstop" switch turned on, so it will always process through to the end of the file, regardless of errors, or until a limit is reached.

==Warnings==
Warnings don't begin with an exclamation mark: they are just comments by LaTeX about things you might want to look into, such as overlong or underrun lines (often caused by unusual hyphenations, for example), pages running short or long, and other typographical niceties (most of which you can ignore until later).
Unlike other systems, which try to hide unevennesses in the text (usually unsuccessfully) by interfering with the letterspacing, LaTeX takes the view that the author or editor should be able to contribute. While it is certainly possible to set LaTeX's parameters so that the spacing is sufficiently sloppy that you will almost never get a warning about badly-fitting lines or pages, you will almost certainly just be delaying matters until you start to get complaints from your readers or publishers.

==Examples==

Only a few common error messages are given here: those most likely to be encountered by beginners. If you find another error message not shown here, and it's not clear what you should do, ask for help.

Most error messages are self-explanatory, but be aware that the place where LaTeX spots and reports an error may be later in the file than the place where it actually occurred. For example if you forget to close a curly brace which encloses, say, italics, LaTeX won't report this until something else occurs which can't happen until the curly brace is encountered (e.g. the end of the document!) Some errors can only be righted by humans who can read and understand what the document is supposed to mean or look like.

Newcomers should remember to check the list of special characters: a very large number of errors when you are learning LaTeX are due to accidentally typing a special character when you didn't mean to. This disappears after a few days as you get used to them.

===Too many }'s ===

<pre>	
! Too many }'s.
l.6 \date December 2004}
</pre>

The reason LaTeX thinks there are too many }'s here is that the opening curly brace is missing after the <tt>\date</tt> control sequence and before the word December, so the closing curly brace is seen as one too many (which it is!). In fact, there are other things which can follow the <tt>\date</tt> command apart from a date in curly braces, so LaTeX cannot possibly guess that you've missed out the opening curly brace until it finds a closing one!

===Undefined control sequence===

<pre>
! Undefined control sequence.
l.6 \dtae
{December 2004}
</pre>

In this example, LaTeX is complaining that it has no such command ("control sequence") as <tt>\dtae</tt>. Obviously it's been mistyped, but only a human can detect that fact: all LaTeX knows is that <tt>\dtae</tt> is not a command it knows about: it's undefined. Mistypings are the most common source of errors. If your editor has drop-down menus to insert common commands and environments, use them!

===Not in Mathematics Mode===

<pre>
! Missing $ inserted
</pre>

A character that can only be used in the mathematics was inserted in normal text. Either switch to mathematic mode via \begin{math}...\end{math} or use the 'quick math mode': \ensuremath{math stuff}

This can also happen if you use the wrong character encoding, for example using utf8 without "\usepackage[utf8]{inputenc}" or using iso8859-1 without "\usepackage[latin1]{inputenc}", there are several character encoding formats, make sure to pick the right one.

===Runaway argument===

<pre>
Runaway argument?
{December 2004 \maketitle
! Paragraph ended before \date was complete.
<to be read again>
\par
l.8
</pre>

In this error, the closing curly brace has been omitted from the date. It's the opposite of the error of too many }'s, and it results in <tt>\maketitle</tt> trying to format the title page while LaTeX is still expecting more text for the date! As \maketitle creates new paragraphs on the title page, this is detected and LaTeX complains that the previous paragraph has ended but \date is not yet finished.

===Underfull hbox===

<pre>	
Underfull \hbox (badness 1394) in paragraph
at lines 28--30
[][]\LY1/brm/b/n/10 Bull, RJ: \LY1/brm/m/n/10
Ac-count-ing in Busi-
[94]
</pre>

This is a warning that LaTeX cannot stretch the line wide enough to fit, without making the spacing bigger than its currently permitted maximum. The badness (0-10,000) indicates how severe this is (here you can probably ignore a badness of 1394). It says what lines of your file it was typesetting when it found this, and the number in square brackets is the number of the page onto which the offending line was printed. The codes separated by slashes are the typeface and font style and size used in the line. Ignore them for the moment. 

This comes up if you force a linebreak, e.g., \\, and have a return before it. Normally TeX ignores linebreaks, providing full paragraphs to ragged text. In this case it is necessary to pull the linebreak up one line to the end of the previous sentence.

===Overfull hbox===

<pre>
[101]
Overfull \hbox (9.11617pt too wide) in paragraph
at lines 860--861
[]\LY1/brm/m/n/10 Windows, \LY1/brm/m/it/10 see
\LY1/brm/m/n/10 X Win-
</pre>

An overfull \hbox means that there is a hyphenation or justification problem: moving the last word on the line to the next line would make the spaces in the line wider than the current limit; keeping the word on the line would make the spaces smaller than the current limit, so the word is left on the line, but with the minimum allowed space between words, and which makes the line go over the edge.

The warning is given so that you can find the line in the code that originates the problem (in this case: 860-861) and fix it. The line on this example is too long by a shade over 9pt. The chosen hyphenation point which minimizes the error is shown at the end of the line (Win-). Line numbers and page numbers are given as before. In this case, 9pt is too much to ignore (over 3mm), and a manual correction needs making (such as a change to the hyphenation), or the flexibility settings need changing.

If the "overfull" word includes a forward slash, such as "<code>input/output</code>", this should be properly typeset as "<code>input\slash output</code>". The use of <code>\slash</code> has the same effect as using the "<code>/</code>" character, except that it can form the end of a line (with the following words appearing at the start of the next line). The "<code>/</code>" character is typically used in units, such as "<code>mm/year</code>" character, which should not be broken over multiple lines.

===Missing package===

<pre>
! LaTeX Error: File Âparalisy.styÂ not found.
Type X to quit or <RETURN> to proceed,
or enter new name. (Default extension: sty)
Enter file name:
</pre>

When you use the <tt>\usepackage</tt> command to request LaTeX to use a certain package, it will look for a file with the specified name and the filetype <tt>.sty</tt>. In this case the user has mistyped the name of the paralist package, so it's easy to fix. However, if you get the name right, but the package is not installed on your machine, you will need to download and install it before continuing. If you don't want to affect the global installation of the machine, you can simply download from Internet the necessary <tt>.sty</tt> file and put it in the same folder of the document you are compiling.

===Package babel Warning: No hyphenation patterns were loaded for the language X===
Although this is a warning from the Babel package and not from LaTeX, this error is very common and (can) give some strange hyphenation (word breaking) problems in your document. Wrong hyphenation rules can decrease the neatness of your document.
<pre>
Package babel Warning: No hyphenation patterns were loaded for
(babel)                the language `Latin'
(babel)                I will use the patterns loaded for \language=0 instead.
</pre>

This can happen after the usage of: (see [[LaTeX/Internationalization]])

<source lang="latex" enclose="none">
\usepackage[latin]{babel}
</source>


