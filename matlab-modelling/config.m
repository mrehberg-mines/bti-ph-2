rv=rover;

rv.breakingRate = 70/3600; %kg/s
rv.breakingPower = 100; %W
rv.loadCapacity = 40; % kg

rv.loadingRate = 100/3600; %kg/s
rv.loadingPower = 50; %W

rv.unloadingRate = 600/3600; %kg/s

rv.speedCoef= 0; % (m/s)/kg
rv.baseSpeed = 0.5 ; %m/s
rv.movingPower = 40; %W

rv.baseMass = 105; %kg
rv.batterySize = 300*3600; %watt-s
rv.chargingPower = -130; %W


elem(1)=Simulink.BusElement;
elem(1).Name = 'Power';
elem(1).DataType = "double";

elem(2)=Simulink.BusElement;
elem(2).Name = 'Location';
elem(2).DataType = "double";

elem(3)=Simulink.BusElement;
elem(3).Name = 'Loaded_Mass';
elem(3).DataType = "double";

elem(4)=Simulink.BusElement;
elem(4).Name = 'Excavated_Mass';
elem(4).DataType = "double";

elem(5)=Simulink.BusElement;
elem(5).Name = 'State';
elem(5).DataType = "int8";

elem(6)=Simulink.BusElement;
elem(6).Name = 'gotoState';
elem(6).DataType = "int8";

curState = Simulink.Bus;
curState.Elements = elem;


out=sim("roverSim");

subplot(3,1,1);
x=out.simout.var.Power.Time./3600;

y1 = out.simout.var.Location.Data;
plot(x,y1)

subplot(3,1,2); 
y2 = out.battery./rv.batterySize;
%y2= out.simout.var.Loaded_Mass.Data;
plot(x,y2)

subplot(3,1,3); 
y3 = out.simout.gotoState.Data;
plot(x,y3)



disp(max(out.total));
disp(sum(out.simout.gotoState.Data==5)/3600);