<?
################################################################################
##
##  prototype JSON service for flashcards
##
################################################################################
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');  

$CSV = $_REQUEST['input'];
if (!file_exists($CSV)) {
  http_response_code(404);
  die();
}

$FC = array();

if (($handle = fopen($CSV, "r")) !== FALSE) {
  $headers = fgetcsv($handle, 2000, ",");
  while (($data = fgetcsv($handle, 2000, ",")) !== FALSE) {
    $FC[] = array_combine($headers, $data);
  }
  fclose($handle);
}

print( json_encode($FC) );


?>
