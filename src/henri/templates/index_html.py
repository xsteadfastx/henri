# Autogenerated file
def render(*a, **d):
    yield """<!DOCTYPE html>
<html>
  <head>
      <link href=\"static/css/milligram.min.css\" rel=\"stylesheet\">
  </head>
  <body>
    <div class=\"container\">
      <h1>henri - the negative processor</h1>
      <form action=\".\", method=\"POST\">
        <fieldset>
          <h3>Process Time</h3>
          <label>Full Process Time (Minutes)</label>
          <input type=\"text\" placeholder=\"7\" name=\"full_process_time\" id=\"full_process_time\">
          <label>Agitation Rythm</label>
          <select id=\"recur_interval\" name=\"recur_interval\">
            <option value=\"30\">30 seconds</option>
            <option value=\"60\">60 seconds</option>
          <br/>
          <br/>
          <input class=\"button-primary\" type=\"submit\" value=\"Lets rock...\">
        </fieldset>
      </form>
    </div>
  </body>
</html>
"""
