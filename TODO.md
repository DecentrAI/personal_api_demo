# Outline of edge node algorithm

## TODOs:

  - [ ] start with simple approach as below where we have a plugin that launches ngrok and uvicorn
    - we can use pre-build "universal" plugin
    - we have to create the webapi script
    - we can communicate via shmem or pipese, queues, etc
    - plugin can send payloads
    - webapi can respond based on data from plugin

  - [ ] App 0: Weather aggregator (asap)
    - plugin config defines list of weather stations
    - webapi request accepts a location and returns aggregated weather data

  - [ ] App 1: EpochManager (2024-04-30)
    - plugin shares epoch data
    - api responds with epoch data (as per oracle test)
    - requires 1 hour of work with AID after App 0 is completed.

  - [ ] App 3: Foundational Model Server API (2024-05-31)
    - pipeline defins model, etc
    - api sends data to plugin
    - plugin puts data into normal local pipeline
    - plugin sends back results to API

  - [ ] SDK: Basic plugin & api definition (2024-06-30)
    - define a API with a NO boilerplate simple piece of code like and config data (url, token, etc):
      ```python
      @app.get("/api/v1/test")
      def test():
        return {"status": "ok"}
      ```
      ```json
      {
        "url": "ngrok-url",
        "token": "ngtoken...",
        "code" : "b64code12345ABCDEF" // this is the code that will be executed so at least basic coding skills are required
      }
      ```
    - code validation uses a spin-off of the exiting code validation engine (PyE2)
  
  - [ ] SDK: Advanced version (2024-10-01)
    - no-code API definition based on pre-defined high-level primitives
    - library of pre-defined plugins/primitives both for AI and non-AI apps

## Biz plugin config

This is the config that actually starts the WebAPI.

  - ngrok key
  - ngrok url
  - ngrok-uvicorn port
  - api entry point (source code ie. plugin/business/my_ngrok_test_webapi.py)



## Biz plugin script
```python

# plugin/business/my_ngrok_test.py

class MyNgrokTestPlugin(BasePlugin):
  """
  I should be able to use a "UniversalWebApiPlugin"
  """

  def on_init(self):
    # launch ngrok
    # create shmem
    # launch uvicorn using api entry point `uvicorn plugin.business.my_ngrok_test_webapi:app --host 0.0.0.0 ...`
    return

  def on_close(self):
    # close shmem
    # close uvicorn
    # close ngrok
    return


  def webapi_process(self):
    # maybe do business logic
    # maybe write back to shmem
    # maybe create a payload with data from webapi
    return


  def process(self):
    # if read from shmem
      # execute webapi_process
    return

```


## API script

```python
import fastapi

app = fastapi.FastAPI()

@app.get("/api/v1/test")
def test():
  return {"status": "ok"}

```