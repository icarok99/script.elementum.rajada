
provider = input('Provider: ')

xml = """
<setting label="[B]PROVIDER_NAME[/B]   [COLOR gray][$ADDON[script.elementum.rajada 32111]][/COLOR]" id="use_PROVIDER_NAME" type="bool" default="true" />
  <setting id="PROVIDER_NAME_alias" label="32077" type="text" default="" subsetting="true" visible="eq(-1,true)" />
  <setting id="PROVIDER_NAME_contains" type="enum" label="32080" subsetting="true" lvalues="32081|32082|32083" visible="eq(-2,true)" />
"""

print(xml.replace('PROVIDER_NAME', provider))
