python compare_spectra.py -i ../output/met/MET_slim_total.root -o met -v met -bl 0 -bh 750 -b 75
python compare_spectra.py -i ../output/met/MET_slim_total.root -o met -v jet_pt -bl 0 -bh 750 -b 75
python compare_spectra.py -i ../output/met/MET_slim_total.root -o met -v jet_phi -bl -3 -bh 3 -b 50
python compare_spectra.py -i ../output/met/MET_slim_total.root -o met -v jet_eta -bl -3 -bh 3 -b 50

python compare_spectra.py -i ../output/met/MET_slim_total.root -o met_norm -v met -bl 0 -bh 750 -b 75
python compare_spectra.py -i ../output/met/MET_slim_total.root -o met_norm -v jet_pt -bl 0 -bh 750 -b 75
python compare_spectra.py -i ../output/met/MET_slim_total.root -o met_norm -v jet_phi -bl -3 -bh 3 -b 50
python compare_spectra.py -i ../output/met/MET_slim_total.root -o met_norm -v jet_eta -bl -3 -bh 3 -b 50


python compare_spectra.py -i ../output/doublemuon/DoubleMu_slim.root -o doublemu -v met -bl 0 -bh 750 -b 75
python compare_spectra.py -i ../output/doublemuon/DoubleMu_slim.root -o doublemu -v jet_pt -bl 0 -bh 750 -b 75
python compare_spectra.py -i ../output/doublemuon/DoubleMu_slim.root -o doublemu -v jet_phi -bl -3 -bh 3 -b 50
python compare_spectra.py -i ../output/doublemuon/DoubleMu_slim.root -o doublemu -v jet_eta -bl -3 -bh 3 -b 50

python compare_spectra.py -i ../output/doublemuon/DoubleMu_slim.root -o doublemu_norm -v met -bl 0 -bh 750 -b 75
python compare_spectra.py -i ../output/doublemuon/DoubleMu_slim.root -o doublemu_norm -v jet_pt -bl 0 -bh 750 -b 75
python compare_spectra.py -i ../output/doublemuon/DoubleMu_slim.root -o doublemu_norm -v jet_phi -bl -3 -bh 3 -b 50
python compare_spectra.py -i ../output/doublemuon/DoubleMu_slim.root -o doublemu_norm -v jet_eta -bl -3 -bh 3 -b 50


python compare_spectra.py -i ../output/doublemuon/DoubleMu_slim.root -o doublemu -v njet -bl 0 -bh 10 -b 10
python compare_spectra.py -i ../output/met/MET_slim_total.root -o met -v njet -bl 0 -bh 10 -b 10


python compare_spectra.py -i ../output/jetht/JetHT_slim_total.root -o jetht -v met -bl 0 -bh 750 -b 75
python compare_spectra.py -i ../output/jetht/JetHT_slim_total.root -o jetht -v jet_pt -bl 0 -bh 750 -b 75
python compare_spectra.py -i ../output/jetht/JetHT_slim_total.root -o jetht -v jet_phi -bl -3 -bh 3 -b 50
python compare_spectra.py -i ../output/jetht/JetHT_slim_total.root -o jetht -v jet_eta -bl -3 -bh 3 -b 50

python compare_spectra.py -i ../output/jetht/JetHT_slim_total.root -o jetht_norm -v met -bl 0 -bh 750 -b 75
python compare_spectra.py -i ../output/jetht/JetHT_slim_total.root -o jetht_norm -v jet_pt -bl 0 -bh 750 -b 75
python compare_spectra.py -i ../output/jetht/JetHT_slim_total.root -o jetht_norm -v jet_phi -bl -3 -bh 3 -b 50
python compare_spectra.py -i ../output/jetht/JetHT_slim_total.root -o jetht_norm -v jet_eta -bl -3 -bh 3 -b 50
