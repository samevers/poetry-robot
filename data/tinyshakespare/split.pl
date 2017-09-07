#! /usr/bin/perl -w
############################################
#
# Author: 
# Create time: 2017 8月 16 20时25分18秒
# E-Mail: @sogou-inc.com
# version 1.0
#
############################################
use Encode;
while(my $line = <>)
{
	chomp $line;
	$line =~ s/注释：(.*)$|注释:(.*)$|【注释】(.*)$//g;
	$line =~ s/【(.*?)】//g;
	$line =~ s/【(.*?)$//g;
	$line =~ s/《(.*?)》//g;
	$line =~ s/《(.*?)$//g;
	$line =~ s/\((.*?)\)//g;
	$line =~ s/\((.*?)$//g;
	$line =~ s/\[(.*?)\]//g;
	$line =~ s/\[(.*?)$//g;
	$line =~ s/（(.*?)）//g;
	$line =~ s/（(.*?)$//g;
	$line =~ s/\{(.*?)\}//g;
	$line =~ s/\{(.*?)$//g;
	$line =~ s/[\-_\.0-9]+//g;
	$line =~ s/^作者(.*?) //g;
	$line =~ s/ (.*?)作者(.*?) //g;
	$line =~ s/ (.*?)作者(.*?)$//g;
	if($line =~ /作者/)
	{
		$line =~ s/^(.*?)\s+//;
	}
	#print "\t".$line."\n";
	$line =~ s/ 作于(.*)$//g;
	$line =~ s/ (.*?)作于(.*)$//g;
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
