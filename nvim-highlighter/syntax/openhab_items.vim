if exists('b:current_syntax')
  finish
endif

syn case match

syn region openhabComment start='/\*' end='\*/' keepend contains=@Spell
syn match openhabComment '//.*$' contains=@Spell

syn region openhabString start='"' skip='\\."' end='"' contains=openhabFormat,openhabSemanticTag,openhabMetadataAIValue,openhabMetadataReportValue,openhabMetadataSemanticsValue
syn region openhabBracketList matchgroup=openhabBracketDelimiter start='\[' end='\]' contains=openhabString,openhabBoolean,openhabNumber,openhabAssignmentKey,openhabMetadataKeyAI,openhabMetadataKeyReport,openhabMetadataKeySemantics,openhabListComma,openhabState transparent keepend
syn match openhabIcon '<[^>[:space:]][^>]*>'
syn match openhabNumber '\v<\d+(\.\d+)?>'
syn match openhabBindingUID '\v[a-zA-Z0-9_+-]+(:[a-zA-Z0-9_+.-]+){2,}'
syn match openhabChannelAttr '\<channel\s*=\s*' nextgroup=openhabBindingUID skipwhite
syn match openhabAssignmentKey '\<[A-Za-z_][A-Za-z0-9_]*\ze\s*='
syn match openhabMetadataNamespace '\<\(ai\|report\|semantics\)\ze\s*=\s*"' containedin=ALL
syn match openhabMetadataKeyAI '\<\(aliases\|readable\|writable\|writeable\|safety\|role\)\ze\s*=' containedin=openhabBracketList
syn match openhabMetadataKeyReport '\<\(priority\|normal_min\|normal_max\|problem_states\|normal_states\|section\)\ze\s*=' containedin=openhabBracketList
syn match openhabMetadataKeySemantics '\<\(relatesTo\|isPointOf\)\ze\s*=' containedin=openhabBracketList
syn match openhabMetadataAIValue '"\zs\(state\|room\|equipment\|read-only\|safe-write\|confirm-required\|forbidden\|primary-control\|secondary-control\|status\|sensor\|internal\)\ze"' contained
syn match openhabMetadataReportValue '"\zs\(climate\|lights\|security\|leaks\|battery\|system\|network\|storage\|diagnostics\|weather\)\ze"' contained
syn match openhabMetadataSemanticsValue '"\zs\(Point_\u\w*\|Property_\u\w*\|Equipment_\u\w*\|Location_\u\w*\)\ze"' contained
syn match openhabSemanticTag '"\zs\(Indoor\|Apartment\|Building\|Garage\|House\|Shed\|SummerHouse\|Corridor\|Floor\|Attic\|Basement\|FirstFloor\|GroundFloor\|SecondFloor\|ThirdFloor\|Room\|Bathroom\|Bedroom\|BoilerRoom\|Cellar\|DiningRoom\|Entry\|FamilyRoom\|GuestRoom\|Kitchen\|LaundryRoom\|LivingRoom\|Office\|Veranda\|Outdoor\|Carport\|Driveway\|Garden\|Patio\|Porch\|Terrace\|Alarm\|Calculation\|Control\|Switch\|Forecast\|Measurement\|Setpoint\|Status\|AirQuality\|AQI\|CO\|CO2\|Ozone\|ParticulateMatter\|Pollen\|Radon\|VOC\|Airconditioning\|Airflow\|App\|Brightness\|Channel\|Color\|ColorTemperature\|Current\|Duration\|Enabled\|Energy\|Frequency\|Gas\|Heating\|Humidity\|Illuminance\|Info\|Level\|Light\|LowBattery\|MediaControl\|Mode\|Moisture\|Motion\|Noise\|Oil\|Opening\|LockState\|OpenLevel\|OpenState\|Position\|GeoLocation\|Power\|Precipitation\|Rain\|Presence\|Pressure\|Price\|Progress\|QualityOfService\|SignalStrength\|RSSI\|Smoke\|SoundVolume\|Speed\|StateOfCharge\|Tampered\|Temperature\|Tilt\|Timestamp\|Ultraviolet\|Ventilation\|Vibration\|Voltage\|Water\|Wind\|AlarmDevice\|AlarmSystem\|Application\|AudioVisual\|Display\|Projector\|Television\|MediaPlayer\|Receiver\|Screen\|Speaker\|Bed\|Camera\|CleaningRobot\|Computer\|ControlDevice\|Button\|Dial\|Keypad\|Slider\|WallSwitch\|Door\|BackDoor\|CellarDoor\|FrontDoor\|GarageDoor\|Gate\|InnerDoor\|SideDoor\|Doorbell\|DrinkingWater\|HotWaterFaucet\|WaterFilter\|WaterSoftener\|HVAC\|AirConditioner\|AirFilter\|Boiler\|Dehumidifier\|Fan\|CeilingFan\|ExhaustFan\|KitchenHood\|FloorHeating\|Furnace\|HeatPump\|HeatRecovery\|Humidifier\|RadiatorControl\|SmartVent\|Thermostat\|WaterHeater\|Horticulture\|Irrigation\|LawnMower\|SoilSensor\|LightSource\|AccentLight\|Chandelier\|Downlight\|FloodLight\|Lamp\|LightStrip\|LightStripe\|Lightbulb\|Pendant\|Sconce\|SpotLight\|TrackLight\|WallLight\|Lock\|NetworkAppliance\|Firewall\|NetworkSwitch\|Router\|WirelessAccessPoint\|PetCare\|Aquarium\|PetFeeder\|PetFlap\|PowerOutlet\|PowerSupply\|Battery\|EVSE\|Generator\|Inverter\|SolarPanel\|TransferSwitch\|UPS\|WindGenerator\|Printer\|Printer3D\|Pump\|WaterFeature\|RemoteControl\|Sensor\|AirQualitySensor\|CO2Sensor\|COSensor\|ContactSensor\|ElectricMeter\|FireDetector\|FlameDetector\|HeatDetector\|SmokeDetector\|GasMeter\|GlassBreakDetector\|HumiditySensor\|IlluminanceSensor\|LeakSensor\|OccupancySensor\|MotionDetector\|TemperatureSensor\|VibrationSensor\|WaterMeter\|WaterQualitySensor\|WeatherStation\|Siren\|Smartphone\|Tool\|Tracker\|Valve\|Vehicle\|Car\|VoiceAssistant\|WebService\|WeatherService\|Wellness\|Chlorinator\|Jacuzzi\|PoolCover\|PoolHeater\|Sauna\|Shower\|SwimmingPool\|WhiteGood\|AirFryer\|CoffeeMaker\|Cooktop\|Dishwasher\|Dryer\|FoodProcessor\|Freezer\|Fryer\|IceMaker\|Microwave\|Mixer\|Oven\|Range\|Refrigerator\|Toaster\|WashingMachine\|Window\|WindowCovering\|Blinds\|Drapes\|Zone\|AlarmZone\)\ze"' contained
syn match openhabGroupName '\v\([A-Za-z0-9_, ]+\)'
syn match openhabListComma ','
syn match openhabFormat '%\(\d\+\)\=\.\=\d*[dfs%]'

syn keyword openhabItemType Color Contact DateTime Dimmer Group Image Location Number Player Rollershutter String Switch Call
syn match openhabItemSubtype ':\zs\(Acceleration\|AmountOfSubstance\|Angle\|Area\|ArealDensity\|CatalyticActivity\|Currency\|DataAmount\|DataTransferRate\|Density\|Dimensionless\|ElectricCapacitance\|ElectricCharge\|ElectricConductance\|ElectricConductivity\|ElectricCurrent\|ElectricInductance\|ElectricPotential\|ElectricResistance\|EmissionIntensity\|Energy\|EnergyPrice\|Force\|Frequency\|Illuminance\|Intensity\|Length\|LuminousFlux\|LuminousIntensity\|MagneticFlux\|MagneticFluxDensity\|Mass\|Power\|Pressure\|RadiantExposure\|RadiationAbsorbedDose\|RadiationDoseAbsorbed\|RadiationEffectiveDose\|RadiationDoseEffective\|Radioactivity\|RadiationSpecificActivity\|SolidAngle\|Speed\|Temperature\|Time\|Volume\|VolumePrice\|VolumetricFlowRate\)\>'
syn keyword openhabKeyword channel autoupdate expire ga list groups homekit icon label namespace profile semantics stateDescription unit
syn keyword openhabState ON OFF OPEN CLOSED UP DOWN STOP PLAY PAUSE NEXT PREVIOUS REWIND FASTFORWARD INCREASE DECREASE MOVE UNDEF NULL REFRESH
syn keyword openhabBoolean true false

hi def link openhabComment Comment
hi def link openhabString String
hi def link openhabIcon SpecialChar
hi def link openhabNumber Number
hi def link openhabBindingUID Underlined
hi def link openhabChannelAttr Keyword
hi def link openhabAssignmentKey Identifier
hi def link openhabMetadataNamespace Type
hi def link openhabMetadataKeyAI Keyword
hi def link openhabMetadataKeyReport PreProc
hi def link openhabMetadataKeySemantics Special
hi def link openhabMetadataAIValue Constant
hi def link openhabMetadataReportValue Constant
hi def link openhabMetadataSemanticsValue Underlined
hi def link openhabSemanticTag Special
hi def link openhabGroupName Identifier
hi def link openhabBracketDelimiter Type
hi def link openhabListComma Delimiter
hi def link openhabFormat Special
hi def link openhabItemType Type
hi def link openhabItemSubtype StorageClass
hi def link openhabKeyword Keyword
hi def link openhabState Constant
hi def link openhabBoolean Boolean

let b:current_syntax = 'openhab_items'
