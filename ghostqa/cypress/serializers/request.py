from rest_framework import serializers

class ActionSerializer(serializers.Serializer):
    TYPE_CHOICES = (
        ('visit', 'visit'),
        ('type', 'type'),
        ('click', 'click'),
        ('assert', 'assert'),
        ('press', 'press'),
        ('wait', 'wait'),
        ('check', 'check'),
        ('uncheck', 'uncheck'),
        ('scroll', 'scroll'),
        ('hover', 'hover'),
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