{% macro test_args_macro(arg1=none, arg2=none, arg3=none) %}
{{ print("arg1=" ~ arg1) }}
{{ print("arg2=" ~ arg2) }}
{{ print("arg3=" ~ arg3) }}
{% endmacro %}
