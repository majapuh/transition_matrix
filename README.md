# transition_matrix

Python program doing basic analysis for output of two models.
Input: two files containing one unique_sample_id, label pair per line. First file are old classifications and the second file are new classifications. The samples and classes appearing in the two files need not be exactly the same.

Program contains:
-	Percentage of labels that match in both files
-	N most common old_label,new_label,count transition pairings
-	A graph comparing distribution over classes for both files, so they can be compared
-	A matrix akin to a confusion matrix that presents the changes in labels from old to new model.

Example:
File #1
1,A
2,A
3,B
4,C
5,B

File #2
2,B
3,B
1,A
4,B
5,C 

