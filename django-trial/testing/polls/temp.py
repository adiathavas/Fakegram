      <br />
    <h3>Login</h3>
      <br />
    <input type="text" placeholder="IG Username"/> <br /><br /><br />

    <h3>Password</h3>
<br />
    <input type="password" placeholder="IG Password"/> <br />
      <br />
<!--    <div ripple ripple-class="ripple" ripple-diameter="50" ripple-stream="true" class="btn-submit">submit</div>-->
      <div class="cont">
          <br />
        <button class="submit"><span>Submit</span></button>
      </div>

      < form
      method = "post" >
      { % csrf_token %}
      {{form.as_p}}
      < / form >






<!--<form action="{% url 'polls:action'  %}" method="post">-->
<!--{% csrf_token %}-->
<!--    <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">-->
<!--    <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>-->
<!--<input type="submit" value="Submit">-->
<!--</form>--



<h1>ts</h1>
<br />
<div class="login-panel" ng-app='materialRipple' >
  <form  method="post">
      {% csrf_token %}
        {{form.as_p}}

      <br />
    <h3>Login:</h3>
      <br />
    <input type="text" placeholder="IG Username"/> <br /><br /><br />

    <h3>Password</h3>
<br />
    <input type="password" placeholder="IG Password"/> <br />
      <br />
<!--    <div ripple ripple-class="ripple" ripple-diameter="50" ripple-stream="true" class="btn-submit">submit</div>-->
      <div class="cont">
          <br />
        <button class="submit"><span>Submit</span></button>
      </div>
      {% if counter %}
        <p>Incorrect Password</p>
      {% endif %}


  </form>
</div>
<!--{% else %}-->
<!--    <p>No polls are available.</p>-->
{% endif %}



<!--{% if latest_question_list %}-->
<!--    <ul>-->s
<!--    {% for question in latest_question_list %}-->
<!--        <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>-->
<!--    {% endfor %}-->
<!--    </ul>-->

