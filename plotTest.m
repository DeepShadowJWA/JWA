close all; 

% "2022-10-30 11.39.25 top20.csv" is the name of the file to be analysed
% topNN should be changed in the last two lines too to match the actual number of players 

H = readtable ('2022-10-30 11.39.25 top20.csv',"VariableNamingRule","preserve"); 
H = sortrows(H,'Dino','ascend');

H = dataCleanUp2(H); 

[a,b] = size(H); 

markerType = {"o";  "square"; "diamond"; "^";  "pentagram"; "hexagram"} ; 
lineType = {"--"; ":"; "-."; "-"};

% "*"; "x"	;"v"; ">"; "<";

l = size (lineType,1 ); 
m = size (markerType,1 ); 


col=copper(a);
% p = randperm(a)'; 
% col = col(p,:);

fig = figure ('DefaultAxesFontSize',18, 'units','normalized','outerposition',[0 0 1 1]); 
% fig.Position = [-1803 203 1324 742]; % [74.3333 583.6667 1264 742.6667];

hold on; 

names = H{:,1}; 
data = H{:,2:end}; 

header = H.Properties.VariableNames; 
hh = header(2:b); 


grid on; 
grid minor; 

for i = 1:a

    ll = lineType{mod(i,l)+1}; 
    mm = markerType{mod(i,m)+1};
    currentType = ll+mm; 
    plot (data(i,:), currentType, 'LineWidth', 2,  'color', col(i,:), ...
        'MarkerSize',15, 'MarkerFaceColor', col(i,:), ...
        'MarkerEdgeColor', [1 1 1]); 
% 
end 
hold off;


for j = 1:b-1,
    tmp = hh{j}; 
    newtmp = [tmp(3:6) '-' tmp(8:9) '-' tmp(11:12)]; 
    hh{j} = newtmp; 
end



legend (names, 'Position',[0.01 0.015 0.06 1.0]); 


xticks([1:b-1]); 
xticklabels(hh); 

title('Top 20'); 
saveas (gcf, 'Top 20.png'); 


