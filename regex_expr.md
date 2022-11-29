request spliter: ".+.\n"
request method: "[A-Z]+\S"
requested file: "\/.+?.\s"
referer header: "Referer: .*"
<--wrong regex syntax cause '' maybe used instead of "": note[probably fixed now not tested]
html href: 'href=[\"|\'].*[\"|\']'
html src: 'src=[\"|\'].*[\"|\'] '
<--


cache the files that go with the main file so i don't have too parse all files every time with regex
(tree like structure)