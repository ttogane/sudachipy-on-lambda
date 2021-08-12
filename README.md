# SudachiPyをAWS Lambdaで実行可能なDocker Containerで動かす。

形態素解析ライブラリをAWS Lambdaで使いたかったため、  [SudachiPy](https://github.com/WorksApplications/SudachiPy)をLambdaで実行可能なdocker イメージとして作成し動作させてみた。

## 目次
1. [Chapter0: とりあえずローカルで動かす](#Chapter0:-とりあえずローカルで動かす)
1. [Chapter1: lambdaでの実行手順](#Chapter1:-lambdaでの実行手順)
    - [Step1: AWS　ECRの準備](#Step1:-AWS-ECRの準備)
    - [Step2: docker イメージを作成](#Step2:-docker-イメージを作成)
    - [Step3: AWS ECRへイメージをpush](#Step3:-AWS-ECRへイメージをpush)
    - [Step4: AWS lambdaの関数を作成](#Step4:-AWS-lambdaの関数を作成)
    
</br>

## Chapter0: とりあえずローカルで動かす
以下でコンテナを起動できる。  
環境のテストなどでとりあえずローカル動かしたい場合は以下で実行する。
```bash
# docker compose up
$ docker compose up -d

# execute lambda function
$ curl -XPOST "http://localhost:8080/2015-03-31/functions/function/invocations" -d '{"text": "すもももももももものうち"}'
["\u3059\u3082\u3082\u3082\u3082\u3082\u3082", "\u3082\u3082", "\u306e", "\u3046\u3061"] # => ['すもももももも', 'もも', 'の', 'うち']
```
</br>

## Chapter1: lambdaでの実行手順
- [Step1: AWS　ECRの準備](#Step1:-AWS-ECRの準備)
- [Step2: docker イメージを作成](#Step2:-docker-イメージを作成)
- [Step3: AWS ECRへイメージをpush](#Step3:-AWS-ECRへイメージをpush)
- [Step4: AWS lambdaの関数を作成](#Step4:-AWS-lambdaの関数を作成)

### Step1: AWS　ECRの準備
AWS ECRへログインして、レポジトリを作成する。
```bash
# login amazon ecr repository
$ aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws-account-id>.dkr.ecr.<region>.amazonaws.com

# create docker repository
$ aws ecr create-repository \
    --repository-name <repository-name> \
    --image-scanning-configuration scanOnPush=true \
    --region <region>;
```

### Step2: docker イメージを作成
lamdaへのせるためにAWS ECRへイメージを作成する。  
```bash
# build container image
$ docker build -t <local-image-name>:latest -f ./docker/lambda/Dockerfile .
```
### Step3: AWS ECRへイメージをpush
Step2で作成したイメージにタグをつけてAWS ECRへpushする。
```bash
# tagggin docker image
$ docker tag <local-image-name>:latest <aws-account-id>.dkr.ecr.<region>.amazonaws.com/<repository-name>:latest

# image push to repository
$ docker push <aws-account-id>.dkr.ecr.<region>.amazonaws.com/<repository-name>:latest
```
### Step4: AWS lambdaの関数を作成
以下はブラウザで行う手順になります。

> 1. [AWS Consoleへログイン](https://aws.amazon.com/jp/console/)
> 2. AWS Lambdaのコンソールへアクセスし「関数 > 関数の作成」へ進む
> 3. 「コンテナイメージ」を選択し関数名に**任意のlambda関数名**をつける.
> 4. 「イメージを参照」ボタンを押して「Amazon ECR イメージリポジトリ」選択を開く
> 5. 「Amazon ECR イメージリポジトリ」で[Step1](#Step1:-AWS-ECRの準備)で作成したリポジトリを選択</br>
ex) `sudachipy-on-lambda` 
> 6. 「イメージ」から「latest」のものを選択して「イメージを選択」ボタンを押す
> 7. 「関数を作成」ボタンを押して関数を作成する。
