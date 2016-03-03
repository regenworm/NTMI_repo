python b-step1.py -input data/train20.txt -output train20.txt.binarized
java -ea -Xmx1G -cp bin/ nlp.assignments.parsing.SimpleParser -train train20.txt.binarized -test data/validation20.txt
echo "Result should be around 76.5% F1"
java -ea -Xmx1G -cp bin/ nlp.assignments.parsing.SimpleParser -train train20.txt.binarized -test data/test20.txt
echo "Result should be around 76.5% F1"