function D = dataCleanUp (H)
% adds a 0 before and after non NaN data for a better visualisation of the
% data


    T = table2array(H(:,2:end));
    V = ~isnan(T); 

    limite = size (V,2); 
    
    for i = 1:size(V,1),
        v = T(i,:); 

        transitions = diff([0; isnan(v'); 0])'; 
        runstarts = find(transitions == 1); 
        runends = find(transitions == -1); 

        for j = 1:size (runstarts,2),
            st = runstarts(1,j); 
            en = runends(1,j); 
            H (i,en) = {0}; 
            if (st>1)
                H (i,st+1) = {0}; 
            end

        end

% 
%         idx = find (v,1,'first'); 
%         if (idx > 1)%&(idx<limite)   
%             H (i,idx) = {0}; 
%         end
%     
%         idx = find (v,1,'last'); 
%         if (idx <limite)
%             H (i,idx+2) = {0}; 
%         end
    end 

    D = H; 
end