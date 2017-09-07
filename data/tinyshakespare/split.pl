#! /usr/bin/perl -w
############################################
#
# Author: 
# Create time: 2017 8�� 16 20ʱ25��18��
# E-Mail: @sogou-inc.com
# version 1.0
#
############################################
use Encode;
while(my $line = <>)
{
	chomp $line;
	$line =~ s/ע�ͣ�(.*)$|ע��:(.*)$|��ע�͡�(.*)$//g;
	$line =~ s/��(.*?)��//g;
	$line =~ s/��(.*?)$//g;
	$line =~ s/��(.*?)��//g;
	$line =~ s/��(.*?)$//g;
	$line =~ s/\((.*?)\)//g;
	$line =~ s/\((.*?)$//g;
	$line =~ s/\[(.*?)\]//g;
	$line =~ s/\[(.*?)$//g;
	$line =~ s/��(.*?)��//g;
	$line =~ s/��(.*?)$//g;
	$line =~ s/\{(.*?)\}//g;
	$line =~ s/\{(.*?)$//g;
	$line =~ s/[\-_\.0-9]+//g;
	$line =~ s/^����(.*?) //g;
	$line =~ s/ (.*?)����(.*?) //g;
	$line =~ s/ (.*?)����(.*?)$//g;
	if($line =~ /����/)
	{
		$line =~ s/^(.*?)\s+//;
	}
	#print "\t".$line."\n";
	$line =~ s/ ����(.*)$//g;
	$line =~ s/ (.*?)����(.*)$//g;
	#print $line."\n";
	my @arr = split /\s+/,$line;
	my $newline = "";
	for(my $i = 0; $i < @arr; $i++)
	{
		my $term = $arr[$i];
		if($term !~ /\//)
		{
			$newline .= $term." ";
		}
	}
	#print $newline."\n";
	my $tmp = decode("gbk", $newline);
	@arr = split //, $tmp;
	for(my $i = 0;$i < @arr; $i++)
	{
		print encode("gbk", $arr[$i])." ";
	}
	print "\n";

}
