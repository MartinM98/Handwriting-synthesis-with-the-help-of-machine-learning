$files = Get-ChildItem "D:\Git Repositories\Handwriting-synthesis-with-the-help-of-machine-learning\data\HandwrittenText\*.png"
foreach ($file in $files) {
$filename=$file.Basename
tesseract $file $filename -l eng wordstrbox
}