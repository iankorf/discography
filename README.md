Discography
===========

The xml dumps from discogg are huge. The releases file is something like 10g
compressed. For this reason, one wouldn't want to try parsing the entire thing
into memory. There are 4 files. Miniature versions are in the `data` directory.

+ artists
+ labels
+ masters
+ releases

The structure of these files is like this:

```
<artists>
<artist>...data...</artist>
<artist>
...data...
</artist>
<artists>
```

Each record in the artists file starts with `<artist>` non-indented and
somewhere after ends with `</artist>`. Therefore, and easy way to chunk the
large file into smaller pieces is to look for the starting and ending tags of
interest, of which there are only 4 (the file names above).

```
python3 proc_disco.py data/aritsts_mini.xml.gz artist
```

Let's look at how a simple, artificial record is read by `xmltodict`.

```
<artist att="val"><name>Jane</name><genre>Punk</genre></artist>
```

This is parsed into a data staructure as follows. Note that attribues end up as
keys prepended with the `@` symbol.

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
        "@att": "val",
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
