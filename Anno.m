clc
clear
close all

%%
buildings = readtable('data/buildings.txt');
product_chains = readtable('data/product_chains.txt');
predefined_productivity = readtable('custom_productivity.txt');
for i = 1 : size(predefined_productivity,1)
    prod.(predefined_productivity.name{i}) = predefined_productivity.productivity(i);
end

endproduct = 'naehmaschinen';
endnumber = 5;

chain = get_chain(endproduct, product_chains);

% Example of adding additional productivity
% prod.('kaffee') = 1.75;

productivity = ones(length(chain),1);
for i = 1 : length(chain)
    if isfield(prod, chain{i})
        productivity(i,1) = prod.(chain{i});
    end
end

% Index of chain buildings in the building data
[~, idx] = ismember(chain, buildings.product);

scale_process(endproduct, endnumber, productivity, buildings(idx, :));


function scale_process(endproduct, number, weights, buildings)
end_idx = strcmp(buildings.product,endproduct);
faktor = buildings.time(end_idx) / weights(end_idx) / number;
number_buildings = buildings.time ./ weights / faktor;

Name = buildings.product;
Productivity = weights * 100;
disp('Productivity displayed in %')
table(Name, Productivity, number_buildings)
end


function sources = get_chain(product, product_chains)
if strcmp(product, '')
    sources = {};
    return
end
sources = {product};
if ~ismember(product, product_chains.product)
    return;
end
idx = strcmp(product_chains.product, product);
sources = [sources; get_chain(product_chains.s1{idx}, product_chains)];
sources = [sources; get_chain(product_chains.s2{idx}, product_chains)];
end
