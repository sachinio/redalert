<?php
$target_dir = "/var/www/uploads/" . $_POST['name'] . "/";

$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
$uploadOk = 1;
$imageFileType = pathinfo($target_file,PATHINFO_EXTENSION);
// Check if image file is a actual image or fake image
if(isset($_POST["submit"])) {
    $check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
    if($check !== false) {
        $uploadOk = 1;
        if (!file_exists($target_dir)) {
            mkdir($target_dir, 0777, true);
        }
    } else {
        $uploadOk = 0;
    }
}
// Check if file already exists
if (file_exists($target_file)) {
    $uploadOk = 0;
}
// Check file size
if ($_FILES["fileToUpload"]["size"] > 3000000) {
    $uploadOk = 0;
}
// Check if $uploadOk is set to 0 by an error
if ($uploadOk == 0) {
// if everything is ok, try to upload file
} else {
    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {} else {}
}

$name = escapeshellarg($_POST['name']);
$title = escapeshellarg($_POST['title']);
$content = escapeshellarg($_POST['content']);
$icon = $_POST['icon'];
$r = "" . escapeshellarg(basename($_FILES["fileToUpload"]["name"]));
$output = shell_exec("sudo python addTimelineItem.py $name $title $content $icon $r 2>&1");
echo "<script>window.location = '../clients/timeline.html'</script>";
?>