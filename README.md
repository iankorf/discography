Discography
===========

The entire dicogs database is dumped into XML files on a monthly basis with a
CC0 No Rights Reserved license. Yay! You can find the dumps here:

https://discogs-data-dumps.s3.us-west-2.amazonaws.com/index.html

There are 4 files per month. 

+ artists
+ labels
+ masters
+ releases

## Splitting huge files ##

The xml dumps from discogg are *HUGE*. The releases file is >11g compressed.
For this reason, you should download them in their compressed format, never
expand them, and obviously not attempt to read the files entirely into memory.
There are miniaturized versions in the `data` directory for development and
testing. The structure of these files is like this:

```
<artists>
<artist>...data...</artist>
<artist>
...data...
</artist>
<artists>
```

Each record in the artists file starts with `<artist>` non-indented and
somewhere after there is a line that ends with `</artist>`. It may be the same
line or another line farther down the file. Therefore, an easy way to split the
large file into smaller pieces is to look for lines starting with and ending
with the tag of interest. In the artists file, the tag is artist. The same
singular and plural relationship is found in the labels, masters, and releases
files.

You can explore the files with `proc_disco.py`, which dumps the XML as JSON.

```
python3 proc_disco.py data/aritsts_mini.xml.gz artist
```

## Parsing with xmltodict ##

`proc_disco.py` uses the `xmltodict` library. If it's not installed you will
have to do a `pip3 install xmltodict`. Let's look at how a simple, artificial
record is read by `xmltodict`.

```
<artist att="val"><name>Jane</name><genre>Punk</genre></artist>
```

The relationship between XML and dictionaries makes sense after you take into
account the properties of an XML file. Let's look at this in some detail. Note
that attribues end up as keys prepended with the `@` symbol.

```
{
    "artist": {
        "@att": "val",
        "name": "Jane",
        "genre": "Punk"
    }
}
```

Let's look at a slightly more complex structure. Notice that the `genre` tag
appears more than once.

```
<artist>
	<name>Tom</name>
	<genre>Rock</genre>
	<genre>Roll</genre>
</artist>
```

When there are redundant tags, they get turned into a list.

```
{
    "artist": {
        "name": "Tom",
        "genre": [
            "Rock",
            "Roll"
        ]
    }
}
```

However, if redundant tags have both attributes and data, it gets more complex
because each item needs to carry its attributes with it.

```
<artist>
	<name>X</name>
	<genre foo="bar">Funk</genre>
	<genre cow="moo">Techno</genre>
</artist>
```

The solution is a list of dictionaries with a special `#text` tag for the data.

```
{
    "artist": {
        "name": "X",
        "genre": [
            {
                "@foo": "bar",
                "#text": "Funk"
            },
            {
                "@cow": "moo",
                "#text": "Techno"
            }
        ]
    }
}
```

## Artists Structure ##



## Labels Structure ##

+ contactinfo
+ data_quality
+ id
+ images
	+ image
		+ @height
		+ @type
		+ @uri
		+ @uri150
		+ @width
+ name
+ parentLabel
	+ #text
	+ @id
+  profile
+ sublabels
	+ label
		+ #text
		+ @id
+ urls
	+ url


## Masters Structure ##

## Releases Structure ##

