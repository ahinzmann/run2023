void EventsPrint(const char * file) {
TFile f(file);
TTree *t;
f.GetObject("Events",t);
cout << "events: " << t->GetEntries() << std::endl;
//t->Draw("mjj>>hist");
//TH1F *hist = (TH1F*)gDirectory->Get("hist");
//cout << hist->Integral() << std::endl;
}
