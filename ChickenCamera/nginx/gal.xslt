<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" encoding="utf-8" indent="yes" />
<xsl:template match="/">
  <xsl:text disable-output-escaping='yes'>&lt;!DOCTYPE html&gt;</xsl:text>
  <html>
  <head>
    <title><xsl:value-of select="$title" /></title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <style>
    img {
            display: block;
            max-width: 20cm;
            max-height: 20cm;
            margin: 2mm;
            vertical-align: bottom;
        }
    @media all and (max-width: 20.4cm) {
        img {
            max-width: calc(100% - 4mm);
        }
    }
    body {
            margin: 0;
    }
    </style>
  </head>
  <body>
    <xsl:for-each select="list/file">
        <xsl:variable name="pic" select="."/>
        <span>File: <xsl:value-of select="$pic"/></span>
        <img src="{.}" alt="{.}"/>
    </xsl:for-each>
  </body>
  </html>
</xsl:template>
</xsl:stylesheet>
