import xml.etree.ElementTree as ET

def replace_thread_group(jmx_content,jmx_properties={}):
    root = ET.fromstring(jmx_content)
    print(root)
    # Create the new ConcurrencyThreadGroup element with default values
    new_thread_txt = f'''
        <com.blazemeter.jmeter.threads.concurrency.ConcurrencyThreadGroup guiclass="com.blazemeter.jmeter.threads.concurrency.ConcurrencyThreadGroupGui" testclass="com.blazemeter.jmeter.threads.concurrency.ConcurrencyThreadGroup" testname="Login_Script" enabled="true">
            <elementProp name="ThreadGroup.main_controller" elementType="com.blazemeter.jmeter.control.VirtualUserController"/>
            <stringProp name="Hold">{jmx_properties.get("durations",0)}</stringProp>
            <stringProp name="Steps">{jmx_properties.get("jrampup_steps",10)}</stringProp>
            <stringProp name="RampUp">{jmx_properties.get("jrampup_time",10)}</stringProp>
            <stringProp name="TargetLevel">{jmx_properties.get("jthreads_total_user",10)}</stringProp>
            <stringProp name="Iterations">{jmx_properties.get("Iterations",0)}</stringProp>
            <stringProp name="Unit">S</stringProp>
            <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
        </com.blazemeter.jmeter.threads.concurrency.ConcurrencyThreadGroup>
    '''
    
    # hold -> duration
    # RampUp -> RampUp Time
    # Steps -> RampUp Steps
    # TargetLevel -> Total User
    # 
    
    new_thread_group = ET.fromstring(new_thread_txt)


    # Find the existing ThreadGroup element
    thread_group = root.find(".//ThreadGroup")
    if thread_group is None:
        thread_group = root.find(".//com.blazemeter.jmeter.threads.concurrency.ConcurrencyThreadGroup")
        
    if thread_group:
        new_thread_group.tail = thread_group.tail
        thread_group.clear()
        thread_group.tag = new_thread_group.tag
        thread_group.attrib = new_thread_group.attrib
        thread_group.text = new_thread_group.text
        thread_group.tail = new_thread_group.tail

        for child in new_thread_group:
            thread_group.append(child)

    modified_jmx_content = ET.tostring(root, encoding="unicode")

    return modified_jmx_content

    