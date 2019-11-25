# Autogenerated file
def render(*a, **d):
    yield """<!DOCTYPE html>
<html>
  <head>
      <link href=\"static/css/milligram.min.css\" rel=\"stylesheet\">
      <script>
      var source = new EventSource(\"events\");
      source.onmessage = function(event) """
    yield """{
          document.getElementById(\"result\").innerHTML = event.data;
      }
      source.onerror = function(error) """
    yield """{
          console.log(error);
          document.getElementById(\"result\").innerHTML += \"EventSource error:\" + error + \"<br>\";
      }
    </script>
  </head>
  <body>
    <div class=\"container\">
      <h1>henri - the negative processor</h1>
      <div><span id=\"result\"></span></div>
    </div>
  </body>
</html>
"""