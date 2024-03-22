FROM alpine/jmeter:5.6.3



# # Download and copy plugins-manager.jar to JMeter lib/ext directory
# RUN wget -O /tmp/jmeter-plugins-manager-0.11.jar https://jmeter-plugins.org/get/
# RUN mv /tmp/jmeter-plugins-manager-0.11.jar /opt/apache-jmeter-5.6.3/lib/ext/

COPY ./jmeter-scripts/jmeter-plugins-manager-0.11.jar /opt/apache-jmeter-5.6.3/lib/ext/jmeter-plugins-manager-0.11.jar

# Check if is cmdrunner-2.0.jar exists in JMETER_HOME/lib directory
# RUN if [ ! -f /opt/apache-jmeter-5.6.3/lib/cmdrunner-2.3.jar ]; then \
#         wget -O /tmp/cmdrunner-2.3.jar https://jmeter-plugins.org/get/; \
#         mv /tmp/cmdrunner-2.3.jar /opt/apache-jmeter-5.6.3/lib/; \
#     fi
COPY ./jmeter-scripts/cmdrunner-2.3.jar /opt/apache-jmeter-5.6.3/lib/cmdrunner-2.3.jar

# Check if PluginsManagerCMD.sh or PluginsManagerCMD.bat exists in JMETER_HOME/lib directory
RUN if [ ! -f /opt/apache-jmeter-5.6.3/lib/PluginsManagerCMD.sh ] && [ ! -f /opt/apache-jmeter-5.6.3/lib/PluginsManagerCMD.bat ]; then \
        java -cp /opt/apache-jmeter-5.6.3/lib/ext/jmeter-plugins-manager-0.11.jar org.jmeterplugins.repository.PluginManagerCMDInstaller; \
    fi



WORKDIR  /opt/apache-jmeter-5.6.3/bin

RUN PluginsManagerCMD.sh install jpgc-json=2.2,jpgc-casutg
RUN PluginsManagerCMD.sh install jpgc-synthesis