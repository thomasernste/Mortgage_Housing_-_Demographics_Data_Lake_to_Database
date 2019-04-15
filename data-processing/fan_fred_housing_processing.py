{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "+-------------+------------+-------------+\n",
      "| census_tract|original_upb|property_type|\n",
      "+-------------+------------+-------------+\n",
      "|'31109002300'|       88000|            2|\n",
      "|'06071009908'|      218000|            2|\n",
      "|'34039036302'|      273000|            2|\n",
      "|'12081001404'|      279000|            2|\n",
      "|'28121020206'|      127000|            2|\n",
      "|'34041031102'|      137000|            2|\n",
      "|'12101031701'|      374000|            2|\n",
      "|'32003006700'|      336000|            2|\n",
      "|'06083000600'|      625000|            2|\n",
      "|'27045960100'|      131000|            2|\n",
      "+-------------+------------+-------------+\n",
      "only showing top 10 rows\n",
      "\n"
     ]
    },
    {
     "ename": "AttributeError",
     "evalue": "'NoneType' object has no attribute 'show'",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mAttributeError\u001b[0m                            Traceback (most recent call last)",
      "\u001b[0;32m<ipython-input-5-8b5e65859577>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m()\u001b[0m\n\u001b[1;32m     50\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     51\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 52\u001b[0;31m \u001b[0mdf_united_FANNIE_FREDDIE\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mshow\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;36m5\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     53\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;31mAttributeError\u001b[0m: 'NoneType' object has no attribute 'show'"
     ]
    }
   ],
   "source": [
    "# Reading the Fannie Mae and Freddie Mac housing datasets, transforming them, reading in the \n",
    "# relevant columns to a dataframe, and uniting those datasets into one.\n",
    "\n",
    "# Data is available here: \n",
    "\n",
    "\n",
    "from pyspark.sql.functions import regexp_replace, col\n",
    "\n",
    "\n",
    "pathname_FANNIE = 's3a://sparkforinsightproject/fnma_sf2017c_loans.txt'\n",
    "\n",
    "\n",
    "pathname_FREDDIE = 's3a://sparkforinsightproject/fhlmc_sf2017c_loans.txt'\n",
    "\n",
    "\n",
    "pathname_output_UNITED = 's3a://sparkforinsightproject/database_data/transformed_fhlmc_fnma_HOUSING_dataset'\n",
    "\n",
    "\n",
    "def etl_fannie_freddie_data(input_FANNIE_txt, input_FREDDIE_txt, output_UNITED_txt):\n",
    "    \n",
    "    rdd_FANNIE_data = sc.textFile(input_FANNIE_txt)\n",
    "\n",
    "\n",
    "    rdd_FANNIE_data = rdd_FANNIE_data.map(lambda x: x.encode('ascii', 'ignore')).\\\n",
    "                            map(lambda l: l.split()).\\\n",
    "                            map(lambda l: (l[2] + l[4] + l[5], int(l[13]), int(l[36])))\n",
    "\n",
    "    df_FANNIE_data = spark.read.csv(rdd_FANNIE_data, mode='DROPMALFORMED', sep=',', header=False)\\\n",
    "                                    .withColumn(\"_c0\",regexp_replace(col(\"_c0\"), \"\\(\", \"\"))\\\n",
    "                                    .withColumn(\"_c2\",regexp_replace(col(\"_c2\"), \"\\)\", \"\"))\n",
    "    \n",
    "        \n",
    "    rdd_FREDDIE_data = sc.textFile(input_FREDDIE_txt)\n",
    "\n",
    "\n",
    "    rdd_FREDDIE_data = rdd_FREDDIE_data.map(lambda x: x.encode('ascii', 'ignore')).\\\n",
    "                            map(lambda l: l.split()).\\\n",
    "                            map(lambda l: (l[2] + l[4] + l[5], int(l[13]), int(l[36])))\n",
    "\n",
    "    df_FREDDIE_data = spark.read.csv(rdd_FREDDIE_data, mode='DROPMALFORMED', sep=',', header=False)\\\n",
    "                                    .withColumn(\"_c0\",regexp_replace(col(\"_c0\"), \"\\(\", \"\"))\\\n",
    "                                    .withColumn(\"_c2\",regexp_replace(col(\"_c2\"), \"\\)\", \"\"))\n",
    "    \n",
    "\n",
    "    \n",
    "    # Join housing datasets, adding column headers, and writing to S3\n",
    "\n",
    "    df_FRANNIE_FREDDIE_UNITED = df_FANNIE_data.union(df_FREDDIE_data)\n",
    "\n",
    "    df_FRANNIE_FREDDIE_UNITED = df_FRANNIE_FREDDIE_UNITED.withColumnRenamed(\"_c0\", \"census_tract\").\\\n",
    "                                                withColumnRenamed(\"_c1\", \"original_upb\").\\\n",
    "                                                withColumnRenamed(\"_c2\", \"property_type\")\n",
    "\n",
    "    df_FRANNIE_FREDDIE_UNITED.show(10)\n",
    "\n",
    "#     df_FHLMC_FNMA_sf2017_UNITED.write\\\n",
    "#     .mode(\"overwrite\")\\\n",
    "#     .save(\"s3a://sparkforinsightproject/database_data/transformed_fhlmc_fnma_HOUSING_dataset\")\n",
    "\n",
    "    \n",
    "    \n",
    "df_united_FANNIE_FREDDIE = etl_fannie_freddie_data(pathname_FANNIE, pathname_FREDDIE)\n",
    "    \n",
    "    \n",
    "df_united_FANNIE_FREDDIE.show(5)\n",
    "\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 2",
   "language": "python",
   "name": "python2"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 2
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython2",
   "version": "2.7.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
