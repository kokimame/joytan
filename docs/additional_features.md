#Additional Features
We support additional features by passing additional parameters(as a dict) to the TTS engines. Now we have only one feature named 'Chikana'.

To support the features, input a string in the "Additional Parameter" panel like  
{'key1':value1,'key2':value2,...}  
. Note that the values might also be a dict.


#Chikana
Chikana support pronouncing the Japanese kanjis in their Chinese pronunciation, while the kanas would remain pronounced in Japanese.
To enable this feature, you should choose your Chinese TTS service first, and add following parameters.

'chikana':True  
'chikanaOpt':  
--'service': String. the name of the TTS service, would be the same as the Chinese TTS service by default. You should use the name of TTS engine shown in the overview panel (the left side of preference panel).(Optional)  
--'c2c': Boolean. True if you want to pronounce kanas character to character (by adding ',' between them).(Optional, default is True)   
--other options: all the options required for the japanese TTS service. You should used the name of options according to the text shown in the the overview panel (the left side of preference panel).

For example, if you are using Amazon Polly, you may add the following addtional parameters.

{'chikana':True,'chikanaOpt':{'voice':'mizuki','variant':'x-slow','c2c': True}}

Note: this feature could make the generation process become very slow, especially when Japanese and Chinese words are mixed toghether.
