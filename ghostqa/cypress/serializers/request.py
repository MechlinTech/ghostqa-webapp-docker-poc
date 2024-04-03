from rest_framework import serializers

class ActionSerializer(serializers.Serializer):
    TYPE_CHOICES = (
        ('visit', 'visit'),
        ('click', 'click'),
        ('type', 'type'),
        ('press', 'press'),
        ('wait', 'wait'),
        ('scroll', 'scroll'),
        ('hover', 'hover'),
        ('select', 'select'),
        ('check', 'check'),
        ('uncheck', 'uncheck'),
        ('dblclick', 'dblclick'),
        ('rightclick', 'rightclick'),
        ('clear_text', 'clear_text'),
        ('drag_and_drop', 'drag_and_drop'),
        ('checkbox', 'checkbox'),
        ('uncheckbox', 'uncheckbox'),
        ('submit_form', 'submit_form'),
        ('select_option', 'select_option'),
        ('upload_file', 'upload_file'),
        ('scroll_into_view', 'scroll_into_view'),
        ('scroll_to_window', 'scroll_to_window'),
        ('go_to_url', 'go_to_url'),
        ('go_back', 'go_back'),
        ('go_forward', 'go_forward'),
        ('refresh_page', 'refresh_page'),
        ('element_text_contains', 'element_text_contains'),
        ('element_exist', 'element_exist'),
        ('element_not_exist', 'element_not_exist'),
        ('element_is_not_visible', 'element_is_not_visible'),
        ('element_is_enabled', 'element_is_enabled'),
        ('element_is_visible', 'element_is_visible'),
        ('element_is_disabled', 'element_is_disabled'),
        ('element_has_value', 'element_has_value'),
        ('element_has_attribute_with_value', 'element_has_attribute_with_value'),
        ('invoke_value', 'invoke_value'),
        ('validate_page_title', 'validate_page_title'),
        ('validate_current_url', 'validate_current_url'),
        ('number_of_element_found', 'number_of_element_found'),
        ('blur_element', 'blur_element'),
        ('fixture', 'fixture'),
        ('focus', 'focus'),
        ('force_click', 'force_click'),
        ('select_first_element', 'select_first_element'),
        ('select_last_element', 'select_last_element'),
        ('location', 'location'),
        ('next_element', 'next_element'),
        ('next_all_element', 'next_all_element'),
        ('not', 'not'),
        ('title', 'title'),
        ('should_not_equal', 'should_not_equal'),
        ('should_include', 'should_include'),
        ('should_be_null', 'should_be_null'),
        ('should_be_empty', 'should_be_empty'),
        ('should_equal', 'should_equal'),
        ('should_be_greater_than', 'should_be_greater_than'),
        ('should_be_less_than', 'should_be_less_than'),
        ('have_attribute', 'have_attribute'),
        ('have_prop', 'have_prop'),
        ('have_css_value', 'have_css_value'),
        ('contain_text', 'contain_text'),
        ('enter', 'enter'),
        ('should_be_selected', 'should_be_selected'),
        ('should_be_checked', 'should_be_checked'),
        ('assert', 'assert'),
        # Add more choices as needed
    )

    type = serializers.ChoiceField(choices=TYPE_CHOICES)
    selector = serializers.CharField(required=False, allow_null=True)
    text = serializers.CharField(required=False, allow_null=True)
    key = serializers.CharField(required=False, allow_null=True)
    duration = serializers.IntegerField(required=False, allow_null=True)
    direction = serializers.CharField(required=False, allow_null=True)
    distance = serializers.IntegerField(required=False, allow_null=True)
    option = serializers.CharField(required=False, allow_null=True)
    assertType = serializers.CharField(required=False, allow_null=True)
    value = serializers.CharField(required=False, allow_null=True)
    
    


class BeforeEachSerializer(serializers.Serializer):
    type = serializers.CharField()
    selector = serializers.CharField()

class TestCaseSerializer(serializers.Serializer):
    name = serializers.CharField()
    beforeEach = BeforeEachSerializer(many=True,required=False)
    actions = ActionSerializer(many=True)
    
class TestSuiteSerializer(serializers.Serializer):
    name = serializers.CharField()
    beforeEach = BeforeEachSerializer(many=True,required=False)
    testCases = TestCaseSerializer(many=True)