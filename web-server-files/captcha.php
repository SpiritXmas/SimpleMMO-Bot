<?php	
    if ($_GET["task"] == "captcha") {
      if ($_GET["state"] == "send") {
          file_put_contents("your_path/simplemmo/captcha_response.txt", $_GET["captcha_response"]);
          echo "success";
      }

      $thefile = fopen("captcha_response.txt", "r");
      $captcha_response = fread($thefile, filesize("captcha_response.txt"));
      if ($_GET["state"] == "receive") {
          echo $captcha_response;
          file_put_contents("captcha_response.txt", "0");
      }

      fclose($thefile);
   } 

   if ($_GET["task"] == "remote") {
      if ($_GET["state"] == "send") {
          file_put_contents("remote_state.txt", $_GET["value"]);
          echo "success";
      }

      $thefile = fopen("remote_state.txt", "r");
      $remote_response = fread($thefile, filesize("remote_state.txt"));
      if ($_GET["state"] == "receive") {
          echo $remote_response;
      }

      fclose($thefile);
   }
?>