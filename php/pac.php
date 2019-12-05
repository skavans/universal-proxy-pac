<?php
  $config_content = file_get_contents("rules.json");
  $config = json_decode($config_content);

  echo "function FindProxyForURL(url, host) {\n";
  foreach ($config as $proxy => $hosts) {
      echo "if (";
      $checks = array();
      foreach ($hosts as $host) {
        array_push($checks, "shExpMatch(host, \"" . $host . "\")");
      }
      echo join(" || ", $checks);
      echo ") {return \"PROXY " . $proxy . "\"}\n";
  }
  echo "return \"DIRECT\"";
  echo "\n}";
?>
