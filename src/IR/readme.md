
<h1> Elastic Search: How to Set-up </h1>

<h2> Install Elastic Search </h2>
<div class="install">
    <h3> Windows </h3>
    <p> 
        1. Download Elastic Search from <a href="https://www.elastic.co/downloads/elasticsearch">here</a>
    </p>
    <p> 
        2. Extract the zip file to a folder
    </p>
    <p> 
        3. Open a command prompt and navigate to the bin folder of the extracted folder
    </p>
    <p> 
        4. Run the command <code>elasticsearch.bat</code>
        (its usually located in <code>〈elasticsearch_folder〉\bin</code> directory
    </p>
    <p> 
        5. Open a browser and navigate to <a href="http://localhost:9200/">http://localhost:9200/</a>
    </p>
    <p> 
        6. If you see JSON response containing information about your Elasticsearch cluster, then you have successfully installed Elastic Search.
    </p>
</div>
<br>
<br>

<div>
    <h3>Configure Elastic Search for Development</h3>
    <p>
        1. Open the config folder in the extracted folder
    </p>
    <p>
        2. Open the elasticsearch.yml file
    </p>

<h5> Change path for changing the location of the index </h5>

        path.data: C:\Users\user\..\..\.. (example)

<p>other than index file, you can change log file location as well</p>

<br>
<h5> Change path for changing the security of the elastic search (username, password, https) </h5>
<p> make every security related features from <b>true</b> to <b>false</b></p>

        xpack.security.enabled: false

        xpack.security.enrollment.enabled: false
        
        # Enable encryption for HTTP API client connections, such as Kibana, Logstash, and Agents
        xpack.security.http.ssl:
          enabled: false
          keystore.path: certs/http.p12
        
        # Enable encryption and mutual authentication between cluster nodes
        xpack.security.transport.ssl:
          enabled: false
          verification_mode: certificate
          keystore.path: certs/transport.p12
          truststore.path: certs/transport.p12

</div>

<br>
<br>

<div>
    <h3>Install ElasticSearch for python</h3>
    <p>
        <code>pip install elasticsearch</code>
    </p>
</div>

<i>*It's better to modify the configurations before running the elastic search server for the first time.</i>


<br>
<div>
    <h3>Usage Guide</h3>

    <h4>Define Configuration</h4>
    <p>Define all the configuration in the <code>config.yaml</code> in config folder</p>

<h4>Start Server</h4>
<p>run the <code>elasticsearch.bat</code> in the <code>bin</code> folder of the elastic search home directory</p>

<h4>Create Index</h4>
<p> To create index and define the dimensions and configs, run <code>Index_Creator.py</code> in <code>Indexer</code> directory</p>

<h4>Index Documents</h4>
<p>Import <code>Indexer</code> classs in Indexer/Indexer.py and index document one by one calling <code>index</code> function. Check example code in the test folder.</p>

<h4>Search Documents</h4>
<p>Import <code>Searcher</code> classs in Searcher/Searcher.py and search document by calling <code>search</code> function. Check example code in the test folder.</p>

</div>
