$year=$args[0]
$day=$args[1]

mkdir .\src\adventofcode\year$year\day$day
echo $nul > .\src\adventofcode\year$year\day$day\__init__.py
echo $nul > .\src\adventofcode\year$year\day$day\py.typed
echo '' > .\src\adventofcode\year$year\day$day\solution.py
