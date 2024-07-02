---
title: Patrick Collins-区块链 笔记
categories:
  - Web3
description: "Patrick Collins-区块链学习笔记"
date: 2024-04-25 14:11:40
tags:
    - 区块链
    - 以太坊
    - 智能合约
---

​	有关区块链和WEB3全栈开发的课程笔记，来源是Patrick Collins 讲解的区块链课程，使用了Solidity，Javascript进行了智能合约的编写，部署和交互。这是比较流行的写法，当然合约不止Solidity一种编写方法，在引入库的之后，Javascript、Python、Golang都可以做到。

<!-- more -->

> - Created by Typora
> - Author: LRay-iu
> - createTime: 2024-01-09 15:31
> - updateTime: 2024-04-25 22:11



## 工具包

课程链接：【（32 小时最全课程）区块链，智能合约 & 全栈 Web3 开发】 https://www.bilibili.com/video/BV1Ca411n7ta

原视频链接（生肉）：https://www.youtube.com/watch?v=gyMwXuJrbJQ

课程Repo链接：https://github.com/smartcontractkit/full-blockchain-solidity-course-js

Remix网址：https://remix.ethereum.org/

测试币水龙头：https://faucets.chain.link

Sepolia区块链浏览器：https://sepolia.etherscan.io/

Chainlink官方文档：https://docs.chain.link

以太坊货币换算：https://eth-converter.com/

AggregatorV3Interface接口源码：https://github.com/smartcontractkit/chainlink/blob/develop/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol

Solidity 使用文档：https://solidity-by-example.org

## 智能合约

智能合约是约定多个参与方的一些列指令。不同的是，传统合同是写在纸上的，而智能合约是代码写的，并且嵌入到一个去中心化区块链平台，在这个去中心化区块链平台中被执行；

将链上去中心化逻辑和链下去中心化数据和计算相结合，这个东西就叫做混合型智能合约。

混合智能合约会用到`Chainlink`。这是一个组件化，去中心化的预言机网络；不仅可以为智能合约提供外部数据，还可以提供链下计算。本课程和笔记都将基于这个进行开展。

> from Chatgpt : 预言机网络（Oracle network）是一种基于区块链技术的系统，它的主要目标是将现实世界的数据引入区块链中，从而使智能合约能够访问并使用这些数据。智能合约通常无法直接获取外部数据，因为它们在区块链内部运行，并且无法直接连接到外部世界的数据源。预言机网络解决了这个问题，允许区块链与外部数据进行交互。

### 应用

不容易被机构欺骗，通过智能合约可以亲身进入这个行业，所有记录都是公开，透明且不可篡改的。

## 第一笔交易

在chrome浏览器中安装插件METAMASK，注册一个账户并开通两个钱包，分别叫Account 1和 Account 2

因为是学习与测试用的钱包，所以哈希地址就不打码了（反正里面也没钱）

<img src="./Patrick Collins_blockchain_note/image-20240109233040953.png" alt="image-20240109233040953" style="zoom:80%;" />

连接测试网络 Sepolia：

<img src="./Patrick Collins_blockchain_note/image-20240109233120241.png" alt="image-20240109233120241" style="zoom:80%;" />

前往测试网络的水龙头，获取测试币[https://faucets.chain.link](https://faucets.chain.link/)

<img src="./Patrick Collins_blockchain_note/image-20240110144901761.png" alt="image-20240110144901761" style="zoom: 67%;" />

在METAMASK中也能看到已经获取到了测试币

<img src="./Patrick Collins_blockchain_note/image-20240110145343247.png" alt="image-20240110145343247" style="zoom:50%;" />

在https://sepolia.etherscan.io/中也可以查询到对应的交易

<img src="./Patrick Collins_blockchain_note/image-20240112093457519.png" alt="image-20240112093457519"  />

对于上图，交易手续费价格计算：
$$
Transaction(交易手续费) = Gas\,\,Price(燃气价格)\,\, * \,\, Usage\,\,by\,\,Txn(使用了的燃气量)
$$
有Account 1 向 Account 2 发送 0.05个测试币

<img src="./Patrick Collins_blockchain_note/image-20240112094858855.png" alt="image-20240112094858855"  />

<img src="./Patrick Collins_blockchain_note/image-20240112095159024.png" alt="image-20240112095159024" style="zoom:50%;" />

<img src="./Patrick Collins_blockchain_note/image-20240112095206377.png" alt="image-20240112095206377" style="zoom:50%;" />

<center><b>OKay，恭喜你已经完整地完成了一笔交易！</b></center>



## 概念知识快速总结

*// P.S说到底，这份笔记更多是为了记载实战方面的，因此，关于概念的概括一下就过了*

### 权益机制

比特币和前期的以太坊使用的是工作量证明机制（具体见"北京大学肖臻老师《区块链技术与应用》公开课 笔记.md"），而在以太坊2.0中，改为了权益机制；

不同于工作量的证明，在权益机制中，参与区块创建以及验证的叫验证者，而成为验证者需要抵押一定数量的以太币用来确保不会恶意发布交易区块；之后系统会根据算法选举出是哪一个验证者来负责创建新的区块（算法在未来可能更新换代，作为开发者没什么必要学习），在其他验证者验证这个区块交易的真实性以及有效性之后会给予他奖励，如果出现不正当行为，可能会被踢出验证者甚至失去那部分抵押的比特币；

以太坊 2.0 的权益机制还包括社区治理，即验证者可以参与提案和投票，对网络的升级和改变提出建议，并共同决定网络的发展方向。

关于验证者退出：验证者可以随时退出，但是抵押的以太币不会立刻归还，这是为了防止恶意进出的问题

### 关于攻击

区块链攻击主要分为女巫攻击以及51%攻击

在权益证明机制中，由于成为验证者需要支付一定量的以太币，并且存在验证这一环节，导致试图创建假帐号影响区块链这一行为需要付出高额成本，这可以很好地预防女巫攻击。

关于51%攻击，当其掌握足够多的算力，直接创造一条区块链，长度比中心链的一半还要长，那么就可以影响中心链到它之上运行，但是随着区块链不断使用，中心链不断加长，51%攻击所需要的算力也在不断提高，直至近乎不可能做到。



## Solidity(Remix)

网站地址：https://remix.ethereum.org/

一个集成开发环境，编写和交互智能合约的地方

### 第一个智能合约

新建一个sol文件，输入以下内容

```solidity
//SPDX-License-Identifier: MIT
//因为solidity更新频率极高，我们需要在文件开头告诉代码，solidity的版本
pragma solidity 0.8.7;

//关键字，告诉接下来是定义智能合约的内容
contract SimpleStorage{
    //↓这个初始化默认是0
    uint256 favNum;
    function store(uint256 _favNum) public{
        favNum = _favNum;
    } 
}
```

如果想定义其他类型的数据变量：

```solidity
    bool judge = true;
    //↓这个初始化默认是0,256代表分配空间，不写的话默认是256
    uint256 favNum;
    string word = "helloworld";
    int256 num2= 1018;
    address myadress = 0xE9f22C0cB28f58a74574d88679B4A3F933e3d51c;
    //byte最大为32
    bytes32 A = "good";
```

在虚拟环境部署合约：

<img src="./Patrick Collins_blockchain_note/image-20240123155705037.png" alt="image-20240123155705037"  />

使用合约中的方法，修改区块中的数据，相当于发布一条“交易”

<img src="./Patrick Collins_blockchain_note/image-20240123155823210.png" alt="image-20240123155823210" style="zoom:67%;" />

观察到交易成功，且产生燃气费

<img src="./Patrick Collins_blockchain_note/image-20240123155927054.png" alt="image-20240123155927054" style="zoom:67%;" />

<img src="./Patrick Collins_blockchain_note/image-20240123155959166.png" alt="image-20240123155959166" style="zoom:67%;" />

在此基础上更进一步

```solidity
     //view,pure
    function retrieve() public view returns (uint256){
        return favNum;
    }
    function add() public pure returns (uint256){
        return (1+1);
    }
```

`view`：`solidity`得一个关键字，代表了这个函数只会读取合约的状态，因而不会产生燃气费；

`pure`：`solidity`得一个关键字，代表了这个函数既不会修改合约状态也读取不了合约状态，通常会做一些常用算法或者是一些不需要读取数据的算法，因而也	不会产生燃气费；

图形界面上的效果：

<img src="./Patrick Collins_blockchain_note/image-20240125150543392.png" alt="image-20240125150543392" style="zoom: 67%;" />



点击蓝色按钮，不发送交易，我们只是在链下读取数值，因此不产生燃气费，调用这些方法是免费的，但如果在消耗gas的函数中调用它，就会产生执行费用。

### 结构体和数组

结构体定义全部是分号，只有使用的时候内部是逗号；

效果如下：

```solidity
struct People {
        uint256 favNum;
        string name;
    }
    // People 结构体的实例化
People public person = People({favNum: 2, name: "Peter"});
```

<img src="./Patrick Collins_blockchain_note/image-20240125153122214.png" alt="image-20240125153122214" style="zoom:67%;" />

声明变量的类型，然后是对象的可见性，最后是变量名。

```solidity
    People[] public people;
    function addperson(string memory _name,uint256 _favNum) public{
        People memory newperson = People({favNum:_favNum,name:_name});
        people.push(newperson);
    }
```

也可以对数组长度进行限制：

```solidity
	People[3] public people;
```

最终效果：

<img src="./Patrick Collins_blockchain_note/image-20240125155456902.png" alt="image-20240125155456902" style="zoom:67%;" />



值得一提的是，在solidity中有6种方式可以用于存储数,分别是`stack`、`memory`、`storage`、`calldata`、`code`、`logs`

其中，`memory`表示可以被修改的临时变量，`calldata`表示不可以被临时修改的临时变量，二者在方法结束过后会自行销毁，案例如下：

```solidity
    function addperson(string memory _name,uint256 _favNum) public{
        _name = 'cat'; //不会报错
        People memory newperson = People({favNum:_favNum,name:_name});
        people.push(newperson);
    }
    function addperson(string calldata _name,uint256 _favNum) public{
        _name = 'cat' ;//会报错:TypeError: Type literal_string "cat" is not implicitly convertible to expected type string calldata.--> contracts/SimpeStorage.sol:18:17:
        People memory newperson = People({favNum:_favNum,name:_name});
        people.push(newperson);
    }
```

而storage表示可以被修改的永久变量，不写关键字的话默认存储在storage；



### Mapping映射

```solidity
//SPDX-License-Identifier: MIT
//因为solidity更新频率极高，我们需要在文件开头告诉代码，solidity的版本
pragma solidity 0.8.7;

//关键字，告诉接下来是定义智能合约的内容
contract SimpleStorage{
    //↓这个初始化默认是0
    uint256 favNum;
    mapping (string=>uint256) public nameToFavNum;
    // People 结构体的定义
    struct People {
        uint256 favNum;
        string name;
    }
    People[] public people;
    function addperson(string memory _name,uint256 _favNum) public{
        People memory newperson = People({favNum:_favNum,name:_name});
        people.push(newperson);
        nameToFavNum[_name]=_favNum;
    }
}
```



提供了一个字符转uint的索引，效果如下：



<img src="./Patrick Collins_blockchain_note/image-20240125222714288.png" alt="image-20240125222714288" style="zoom: 67%;" />



### 在测试网络上布置智能合约

<img src="./Patrick Collins_blockchain_note/image-20240125230207782.png" alt="image-20240125230207782" style="zoom: 67%;" />

修改环境，选择账户，部署，

<img src="./Patrick Collins_blockchain_note/image-20240125230239939.png" alt="image-20240125230239939" style="zoom:80%;" />

账单：

<img src="./Patrick Collins_blockchain_note/image-20240125230536425.png" alt="image-20240125230536425" style="zoom: 67%;" />

<img src="./Patrick Collins_blockchain_note/image-20240125230559283.png" alt="image-20240125230559283"  />

发送交易：

<img src="./Patrick Collins_blockchain_note/image-20240125231013855.png" alt="image-20240125231013855" style="zoom:80%;" />

点击蓝色按钮，不会产生交易面板提示

<img src="./Patrick Collins_blockchain_note/image-20240125231634552.png" alt="image-20240125231634552" style="zoom: 67%;" />

查看合约：

<img src="./Patrick Collins_blockchain_note/image-20240125230758121.png" alt="image-20240125230758121" style="zoom:80%;" />

进入交易链接，可以看到具体交易内容：

<img src="./Patrick Collins_blockchain_note/image-20240125231517791.png" alt="image-20240125231517791" style="zoom:80%;" />

这是由于区块链的公开透明的特性。

### 合约交互

创建新的文件`SimpleFactory.sol`

```solidity
/*
SimpleFactory.sol
*/
//SPDX-License-Identifier:MIT
pragma solidity ^0.8.7;
//引用其他合约
import "./SimpleDemo.sol";

contract SimpleFactory{
    SimpleDemo[] public simpleDemoArray;
    function createSimpleStorageContract() public{
        SimpleDemo simpleDemo = new SimpleDemo();
        //存进去的其实是每一个simpleDemo的地址
        simpleDemoArray.push(simpleDemo);
    }
    function sfStore (uint256 _simpleDemoIndex,uint256 _simpleStorageNumber) public {
        //Address
        //ABI 应用二进制接口
        //通过下标查的simpleDemo的地址
        SimpleDemo simpleDemo = simpleDemoArray[_simpleDemoIndex];
        //调用其他合约里的方法
        simpleDemo.FavNumEdit(_simpleStorageNumber);
    }
    function sfGet(uint256 _simpleDemoIndex) public view returns(uint256){
        return simpleDemoArray[_simpleDemoIndex].retrieve();
    }
}
```

结果：

<img src="./Patrick Collins_blockchain_note/image-20240127234611622.png" alt="image-20240127234611622" style="zoom:67%;" />

### 继承和重载

在`SimpleDemo.sol`中

```solidity
/*
父类SimpleDemo.sol
*/
contract SimpleDemo{
    //↓这个初始化默认是0
    uint256 favNum;
    function store(uint256 _favNum) public virtual{
        favNum = _favNum;
    } 
}
```

在子类`ExtraDemo.sol`中

```solidity
/*
子类ExtraDemo.sol
*/
import "./SimpleDemo.sol";
contract ExtraDemo is SimpleDemo{
    //override
    //virtual override
    function store(uint256 _favNum) public override{
        favNum = _favNum + 5;
    }
}
```

*//在父类中用`virtual`标注可以重载的方法，在子类中用`override`标注并实现重载*

效果：

<img src="./Patrick Collins_blockchain_note/image-20240129210306564.png" alt="image-20240129210306564" style="zoom:67%;" />

### 使用dataFeed并向合约打钱

本节资料来源：[使用Data Feeds 关于 EVM 链 | Chainlink 文档](https://docs.chain.link/data-feeds/using-data-feeds)

> 为了发送ETH或其他区块链原生通证，函数需要被标记为payable
>
> Chainlink可以在去中心化环境中为智能合约获取外部数据和进行外部计算
>
> Chainlink喂价是从现实世界中读取定价信息或其他数据的方法
>
> Chainlink VRF 是一种将可证明的随机数从现实世界获取到智能合约中的方法。
>
> Chainlink Keepers是一种去中心化驱动事件的方法

<img src="./Patrick Collins_blockchain_note/image-20240205130649419.png" alt="image-20240205130649419" style="zoom:50%;" />

```solidity
/*
Fundeme.sol
从用户那里拿钱
把赚来的钱从合约取出来
*/
//SPDX-License-Identifier:MIT
pragma solidity 0.8.7;
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
//EVM,Ethereum Virtual Machine
contract FundMe{
    //注意交易的单位是wei
    uint256 public minimumUsd = 50;
    function fund() public payable{// 把钱转进合约里
        //检查msg.value是否大于一定数量的美元,为否时会revert fund()回滚并报错
        // msg.value == 0.03*1e18
        require(getConversionRate(msg.value)>= minimumUsd,"Didn't send enough");
    }

    function getPrice() public view returns(uint256){//得到汇率(USD/ETH)
        //ABIw
        //Address 0x694AA1769357215DE4FAC081bf1f309aDC325306
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x694AA1769357215DE4FAC081bf1f309aDC325306);
        ( ,int256 answer,,,) = priceFeed.latestRoundData();
        
        return uint256(answer*1e10);
    }

    function getVersion() public view returns (uint256){//获取了链外数据源的版本信息，并将其作为uint256类型返回
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x694AA1769357215DE4FAC081bf1f309aDC325306);
        return priceFeed.version();
    }
    function getConversionRate(uint256 ethAmount)public view returns (uint256){
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1e18;
        return ethAmountInUsd;
    }
}
```

此处`( ,int256 answer,,,) = priceFeed.latestRoundData();`使用`,`接受不需要的返回值

```solidity
  //注意latestRoundData()返回值
  function latestRoundData()
    external
    view
    returns (
      uint80 roundId,
      int256 answer,
      uint256 startedAt,
      uint256 updatedAt,
      uint80 answeredInRound
    );
```

执行Fundme合约

<img src="./Patrick Collins_blockchain_note/image-20240205140809591.png" alt="image-20240205140809591" style="zoom: 67%;" />

50/2290==0.0218150087260035，因此低于这个价格的交易会失败并回滚

<img src="./Patrick Collins_blockchain_note/image-20240205140823024.png" alt="image-20240205140823024" style="zoom:67%;" />

### 库

库的作用的是可以将一些方法写入指定文件，方便开发时调用它们

新建文件`PriceConverter.sol`

```solidity
/*
PriceConverter.sol
*/
//SPDX-License-Identifier: MIT
pragma solidity 0.8.7;
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
library PriceConverter{
    function getPrice() internal view returns(uint256){//得到汇率(USD/ETH)
        //ABIw
        //Address 0x694AA1769357215DE4FAC081bf1f309aDC325306
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x694AA1769357215DE4FAC081bf1f309aDC325306);
        ( ,int256 answer,,,) = priceFeed.latestRoundData();
        
        return uint256(answer*1e10);
    }

    function getVersion() internal view returns (uint256){//获取了链外数据源的版本信息，并将其作为uint256类型返回
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x694AA1769357215DE4FAC081bf1f309aDC325306);
        return priceFeed.version();
    }
    function getConversionRate(uint256 ethAmount) internal view returns (uint256){
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1e18;
        return ethAmountInUsd;
    }
}
```

将刚才`Fundme.sol`中的`getPrice() , getVersion() , getConversionRate(uint256 ethAmount)`取出并放入新文件中。

```solidity
/*
Fundme.sol
*/
//EVM,Ethereum Virtual Machine
contract FundMe{
    using PriceConverter for uint256;//会将PriceConverter放到uint256下
    //注意交易的单位是wei
    uint256 public minimumUsd = 50;
    address[] public funders;
    mapping(address=>uint256) public addressToAccountFunded;
    function fund() public payable{// 把钱转进合约里
        //检查msg.value是否大于一定数量的美元,为否时会revert fund()回滚并报错
        // msg.value == 0.03*1e18
        require(msg.value.getConversionRate()>= minimumUsd,"Didn't send enough");
        funders.push(msg.sender);
        addressToAccountFunded[msg.sender]=msg.value;
    }
    // function withdraw(){}
}
```

`msg.value.getConversionRate()`会自动将`msg.value`作为`getConversionRate()`的第一参数，第二第三参数则依次写入括号内。

### 从合约提取资金

三种提取资金的方式

```solidity
        //transfer
        payable(msg.sender).transfer(address(this).balance);
        //send
        bool sendSuccess = payable(msg.sender).send(address(this).balance);
        require(sendSuccess,"Send failed");
        //call
        (bool callSuccess, )=payable(msg.sender).call{value:address(this).balance}.("")
        require(callSuccess,"call failed");
```

前两种会受到燃气费的制约，推荐最后一种

```solidity
/*
从用户那里拿钱
把赚来的钱从合约取出来
*/
//SPDX-License-Identifier:MIT
pragma solidity 0.8.7;
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "./PriceConverter.sol";
//EVM,Ethereum Virtual Machine
contract FundMe{
    using PriceConverter for uint256;
    //注意交易的单位是wei
    uint256 public minimumUsd = 50;
    address public owner;
    address[] public funders;
    mapping(address=>uint256) public addressToAccountFunded;
    constructor(){
        owner = msg.sender;
    }
    function fund() public payable{// 把钱转进合约里
        //检查msg.value是否大于一定数量的美元,为否时会revert fund()回滚并报错
        // msg.value == 0.03*1e18
        require(msg.value.getConversionRate()>= minimumUsd,"Didn't send enough");
        funders.push(msg.sender);
        addressToAccountFunded[msg.sender]=msg.value;
    }
    function withdraw() public onlyOwner{
        // for(/*start index, ending index, step amount*/)
        for (uint256 funderIndex = 0;funderIndex < funders.length;funderIndex ++){
            address funder = funders[funderIndex];
            addressToAccountFunded[funder] = 0;//清零账户余额
        }
        //重置数组
        funders = new address[](0); //0个初始元素
        //call
        (bool callSuccess,)=payable(msg.sender).call{value:address(this).balance}("");
        require(callSuccess,"call failed");
    }
    modifier onlyOwner{
        require(msg.sender == owner,"Sender is not owner");
        _;  
    }
}
```

onlyOwner对withdraw的执行者进行了约束，在withdraw执行前会判断合约发起人喝执行人是否相同，只有执行人才可以使用此方法，否则回滚并报错。

<img src="./Patrick Collins_blockchain_note/image-20240219154857856.png" alt="image-20240219154857856" style="zoom:80%;" />

<img src="./Patrick Collins_blockchain_note/image-20240219154902367.png" alt="image-20240219154902367" style="zoom: 80%;" />

### 优化措施

#### 修改require

```solidity
pragma solidity 0.8.7;
import "*******"
//EVM,Ethereum Virtual Machine
error NotOwner();
contract FundMe{
    ***********
    function fund() public payable{// 把钱转进合约里
        ***********
    }
    function withdraw() public onlyOwner{
		***********
    }
    modifier onlyOwner{
        // require(msg.sender == i_owner,"Sender is not owner");
        if(msg.sender == i_owner){revert NotOwner();}
        _;  
    }
}
```

使用require会单独保存`Sender is not owner`，相比`error`会增加`gas`

### recieve和fallback

<img src="./Patrick Collins_blockchain_note/image-20240220135504952.png" alt="image-20240220135504952" style="zoom:80%;" />

```solidity
//SPDX-License-Identifier:MIT
pragma solidity 0.8.7;

contract FallbackExample{
    uint256 public result;

    receive() external payable {
        result = 1;
    }

    fallback() external payable { 
        result = 2;
    }
}
```

## Javascript异步编程

关键字`async`，`await`

只有标注了`async`了的方法中才能使用`await`关键词

```js
async function main() {
  await console.log("hi");
  let variable = 5;
  console.log(variable);
}
main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.log(error);
  });
```

## 将私密数据保存到环境变量中

创建.env文件

```env
PRIVATE_KEY=0xE9f22C0cB28f58a74574d88679B4A3F933e3d51cyarn
```

引包，使用

```js
require("dotenv").config(); // 调用 config 方法加载环境变量 
console.log(process.env.PRIVATE_KEY);
```

## 进阶：私钥管理

资料来源 P57

## HardHat

### 配置项目

1）准备一个空文件夹，终端`yarn add --dev hardhat`

2）`yarn hardhat`

<img src="./Patrick Collins_blockchain_note/image-20240225225217144.png" alt="image-20240225225217144"  />

3）检查solidity版本

<img src="./Patrick Collins_blockchain_note/image-20240225231333402.png" alt="image-20240225231333402"  />

4）编译，`yarn hardhat compile`

5）`yarn add --dev hardhat-deploy`用于简化和管理以太坊智能合约的部署过程

6）删除`deploy.js`, 在`hardhat.config.js`中写入`require("hardhat-deploy");`之后执行`yarn hardhat`，在新`task`中应有`deploy`

7）建立deploy文件夹，之后的编译脚本就写在这里面

<img src="./Patrick Collins_blockchain_note/image-20240225234449556.png" alt="image-20240225234449556"  />

8）编写脚本，并编译`yarn hardhat deploy`

```js
//01-deploy-fund-me.js
//引包，import
//方法定义
//方法使用
function deployFunc() {
    console.log("hi")
}
module.exports.default = deployFunc //将deplyFunc设置为默认要找的函数

```

```terminal
PS D:\study_test\Hardhat\hardhat-fund-me-fcc> yarn hardhat deploy
yarn run v1.22.21
$ D:\study_test\Hardhat\hardhat-fund-me-fcc\node_modules\.bin\hardhat deploy
Compiled 3 Solidity files successfully (evm target: london).
hi
Done in 3.12s.
```

使用`yarn add --dev @chainlink/contracts@0.8.0`下载chainlink预言机中的合约

### Hardhat部署智能合约

#### 关于node.js的脚本的接口开放和使用

这是一个TIP：

```js
// helper-hardhat-config.js
const networkConfig = {
    11155111: {
        name: "Sepolia",
        ethUsdPriceFeed: "0x694AA1769357215DE4FAC081bf1f309aDC325306",
    },
    5: {
        name: "Goerli",
        ethUsdPriceFeed: "0xD4a33860578De61DBAbDc8BFdb98FD742fA7028e",
    },
}
module.exports = {//开放对其他脚本使用的接口
    networkConfig,
}
```

```js
//01-deploy-fund-me.js
//使用刚才的接口
//helpconfig代表了helper-hardhat-config.js这个文件
const helperconfig = require("../helper-hardhat-config.js")
const networkconfig = helperconfig.networkConfig
```

当然也可以这么写

```js
const { networkconfig } = require("../helper-hardhat-config.js")
```

#### 本地/测试网络部署

如果我们没有使用任何测试网

我们需要写一个`Mock`脚本，即如果某个合约不存在，我们就部署一个最小化的版本来进行我们的本地测试，

**hardhat-config.js**

```js
require("@nomicfoundation/hardhat-toolbox");
require("hardhat-deploy");
require("dotenv").config();

/** @type import('hardhat/config').HardhatUserConfig */

// const COINMARKETCAP_API_KEY = process.env.COINMARKETCAP_API_KEY;
const SEPOLIA_RPC_URL = process.env.SEPOLIA_RPC_URL;
const PRIVATE_KEY = process.env.PRIVATE_KEY;
const ETHERSCAN_API_KEY = process.env.ETHERSCAN_API_KEY;

module.exports = {
  solidity: {
    compilers: [
      {
        version: "0.8.7",
      },
      {
        version: "0.6.6",
      },
    ],
  },
  defaultNetwork: "hardhat",
  networks: {
    hardhat: {
      chainId: 31337,
      // gasPrice: 130000000000,
    },
    sepolia: {
      url: SEPOLIA_RPC_URL,
      accounts: [PRIVATE_KEY],
      chainId: 11155111,
      blockConfirmations: 6,
    },
  },
  gasReporter: {
    enabled: true,
    currency: "USD",
    outputFile: "gas-report.txt",
    noColors: true,
    // coinmarketcap: COINMARKETCAP_API_KEY,
  },
  etherscan: {
    apiKey: ETHERSCAN_API_KEY,
  },
  namedAccounts: {
    deployer: {
      default: 0, // here this will by default take the first account as deployer
      1: 0, // similarly on mainnet it will take the first account as deployer. Note though that depending on how hardhat network are configured, the account 0 on one network can be different than on another
    },
  },
  mocha: {
    timeout: 500000,
  },
};

```

**helper-hardhat-config.js**

```js
// helper-hardhat-config.js
const networkConfig = {
  31337: {
    name: "localhost",
  },
  // Price Feed Address, values can be obtained at https://docs.chain.link/data-feeds/price-feeds/addresses
  11155111: {
    name: "sepolia",
    ethUsdPriceFeed: "0x694AA1769357215DE4FAC081bf1f309aDC325306",
  },
};

const developmentChains = ["hardhat", "localhost"];

module.exports = {
  networkConfig,
  developmentChains,
};

```



**MockV3Aggregator.sol**

```solidity
//MockV3Aggregator.sol
//SPDX-License-Identifier:MIT
pragma solidity ^0.6.0;

import "@chainlink/contracts/src/v0.6/tests/MockV3Aggregator.sol";
```

**00-deploy-mocks.js**

//用以部署到本地网络（快）

```solidity
//00-deploy-mocks.js
//这段是部署本地预言机
const { network } = require("hardhat");

const DECIMALS = "8";
const INITIAL_PRICE = "200000000000"; // 2000

module.exports = async ({ getNamedAccounts, deployments }) => {
  const { deploy, log } = deployments;
  const { deployer } = await getNamedAccounts();
  const chainId = network.config.chainId;
  log(network.name);
  if (chainId == 31337) {
    log("Local network detected!Deploying mocks...");
    await deploy("MockV3Aggregator", {
      contract: "MockV3Aggregator",
      from: deployer,
      log: true,
      args: [DECIMALS, INITIAL_PRICE],
    });
    log("Mocks deployed!");
    log("--------------------------------------------------------");
  }
};
// 这段代码指定了当前部署脚本相关的标签。在这里，使用了两个标签："all" 和 "mocks"。
// "all" 标签： 这个标签可能用于将部署脚本与整个项目的所有部署任务关联起来。
// 当运行 npx hardhat deploy --tags all 时，将运行所有带有 "all" 标签的部署任务。
// "mocks" 标签： 这个标签可能用于将部署脚本与与模拟合约相关的其他部署任务关联起来。
// 当运行 npx hardhat deploy --tags mocks 时，将运行所有带有 "mocks" 标签的部署任务。
//yarn hardhat deploy --tags mocks
module.exports.tags = ["all", "mocks"];
```

使用`yarn hardhat deploy --tags mocks`可以精准执行`00-deploy-mocks.js`

也可以对当前`chainId`加以判断，使其能够自动判断部署在哪条链上

**01-deploy-fund-me.js**

//用以部署到测试网络（慢）

```solidity
//01-deploy-fund-me.js
//helpconfig代表了helper-hardhat-config.js这个文件
// const helperconfig = require("../helper-hardhat-config.js")
// const networkconfig = helperconfig.networkConfig
//node.js的快捷写法，写法等同于上方的
const {
  networkConfig,
  developmentChains,
} = require("../helper-hardhat-config.js");
const { network } = require("hardhat");
const { verify } = require("../utils/verify.js");
//async function deployFunc(hre) {
//     hre.getNameAccounts()
//     hre.deployments
// }
// module.exports.default = deployFunc //将deplyFunc设置为默认要找的函数

//hre代表hardhat运行环境
//写法等同于上方的
// module.exports = async (hre) => {
//     const {getNameAccounts,deployments} = hre
// }
//node.js的语法糖，写法等同于上方的
module.exports = async ({ getNamedAccounts, deployments }) => {
  //将deploy和log从deployments这个对象中提取出来，等同于
  //const deploy = deployments.deploy;
  //const log = deployments.log
  const { deploy, log } = deployments;
  //getNameAccounts() 返回一个包含 deployer 属性的对象，等同于
  //const getNameAccountsResult = await getNameAccounts();
  //const deployer = getNameAccountsResult.deployer;
  log("Deploy Fundme...");
  const { deployer } = await getNamedAccounts();
  const chainId = network.config.chainId;

  //---------------确认预言机地址-----------------
  if (developmentChains.includes(network.name)) {
    const ethUsdAggregator = await deployments.get("MockV3Aggregator");
    ethUsdPriceFeedAddress = ethUsdAggregator.address;
  } else {
    // ethUsdPriceFeedAddress的格式：0x694AA1769357215DE4FAC081bf1f309aDC325306
    ethUsdPriceFeedAddress = networkConfig[chainId]["ethUsdPriceFeed"];
  }

  // log(ethUsdPriceFeedAddress);
  //-----------------deploy-----------------------
  const args = [ethUsdPriceFeedAddress];
  const Fundme = await deploy("Fundme", {
    from: deployer,
    args: args, //喂价地址
    log: true,
    waitConfirmation: network.config.blockConfirmations || 1,
  });
  //-------------------verify-----------------------
  //当合约部署网络与指定的不符时会进行检查
  if (
    !developmentChains.includes(network.name) &&
    process.env.ETHERSCAN_API_KEY
  ) {
    //verify
    await verify(Fundme.address, args);
  }
  log("--------------------------------------------------------");
};

module.exports.tags = ["all", "fundme"];
```

输入`yarn hardhat deploy --network sepolia`或者`yarn hardhat deploy --network hardhat`，会识别到`network.name`的值并部署`Fundme`合约到**具体的网络**中，同时使用`MockV3Aggregator.sol`或者 `ethUsdPriceFeed: "0x694AA1769357215DE4FAC081bf1f309aDC325306"`作为喂价合约

`utils`文件夹，用于验证合约的合法性和安全性

**verify.js**

```js
//verify.js
const { run } = require("hardhat");
const verify = async (contractAddress, args) => {
  console.log("Verifying Contract...");
  try {
    await run("verify:verify", {
      address: contractAddress,
      constructorArguments: args,
    });
  } catch (e) {
    if (e.message.toLowerCase().includes("already verified")) {
      console.log("Already Verified!");
    } else {
      console.log(e);
    }
  }
};
module.exports = { verify };

```

效果如下：

（1）部署到本地网络

```terminal
PS D:\study_test\Hardhat\Harhat-Fundme> yarn hardhat deploy --network hardhat
yarn run v1.22.21
warning package.json: No license field
$ D:\study_test\Hardhat\Harhat-Fundme\node_modules\.bin\hardhat deploy --network hardhat
https://eth-sepolia.api.onfinality.io/public
Nothing to compile
Local network detected!Deploying mocks...
deploying "MockV3Aggregator" (tx: 0x3d732abdeda8235691578f5eae48ec57c18e6860c18196ab7b211ca8f74dce2b)...: deployed at 0x5FbDB2315678afecb367f032d93F642f64180aa3 with 569759 gas
Mocks deployed!
--------------------------------------------------------
Deploy Fundme...
deploying "Fundme" (tx: 0x9275acdb459bd3d25e3dbf786faa9a18efb9edf2bcaa93cf56f4a7dc5b97b1e8)...: deployed at 0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512 with 846785 gas
--------------------------------------------------------
Done in 2.94s.
```

（2）部署到测试网络

```terminal
$ D:\study_test\Hardhat\Harhat-Fundme\node_modules\.bin\hardhat deploy --network sepolia
https://eth-sepolia.api.onfinality.io/public
Nothing to compile
Deploy Fundme...
deploying "Fundme" (tx: 0x8c2e8759b86f8076702ed50b0abaa5d082ed8ac47589f380f367e2b62aeefc3d)...: deployed at 0x58962eaA9001b9C3F1Eb908Ac1347213b2D39A5D with 846785 gas
Verifying Contract...
UnexpectedError: An unexpected error occurred during the verification process.
Please report this issue to the Hardhat team.
Error Details: Connect Timeout Error
    at Etherscan.isVerified (D:\study_test\Hardhat\Harhat-Fundme\node_modules\@nomicfoundation\hardhat-verify\src\internal\etherscan.ts:126:13)
    at processTicksAndRejections (node:internal/process/task_queues:95:5)
    at SimpleTaskDefinition.action (D:\study_test\Hardhat\Harhat-Fundme\node_modules\@nomicfoundation\hardhat-verify\src\internal\tasks\etherscan.ts:101:24)
    at Environment._runTaskDefinition (D:\study_test\Hardhat\Harhat-Fundme\node_modules\hardhat\src\internal\core\runtime-environment.ts:358:14)
    at Environment.run (D:\study_test\Hardhat\Harhat-Fundme\node_modules\hardhat\src\internal\core\runtime-environment.ts:191:14)        
    at SimpleTaskDefinition.action (D:\study_test\Hardhat\Harhat-Fundme\node_modules\@nomicfoundation\hardhat-verify\src\index.ts:284:9) 
    at Environment._runTaskDefinition (D:\study_test\Hardhat\Harhat-Fundme\node_modules\hardhat\src\internal\core\runtime-environment.ts:358:14)
    at Environment.run (D:\study_test\Hardhat\Harhat-Fundme\node_modules\hardhat\src\internal\core\runtime-environment.ts:191:14)        
    at verify (D:\study_test\Hardhat\Harhat-Fundme\utils\verify.js:6:5)
    at Object.module.exports [as func] (D:\study_test\Hardhat\Harhat-Fundme\deploy\01-deploy-fund-me.js:64:5)
--------------------------------------------------------
Done in 84.60s.
```

合约`0x8c2e8759b86f8076702ed50b0abaa5d082ed8ac47589f380f367e2b62aeefc3d`

被部署在以太坊地址`0x58962eaA9001b9C3F1Eb908Ac1347213b2D39A5D`

<img src="./Patrick Collins_blockchain_note/image-20240305002127313.png" alt="image-20240305002127313" style="zoom:67%;" />

#### 编写脚本注入资金

P.S 在本地Hardhat环境中运行

```js
//fund.js
const { ethers, getNamedAccounts } = require("hardhat");

async function main() {
  const { deployer } = await getNamedAccounts();
  console.log(`Deployer address: ${deployer}`);
  const fundme = await ethers.getContractAt("Fundme", deployer);
  // console.log(`Got contract Fundme at ${fundme.address}`);
  console.log("Funding contract...");
  const transactionResponse = await fundme.fund({
    value: ethers.parseEther("0.1"),
  });
  await transactionResponse.wait(1);
  console.log("Funded!");
  const balance = await ethers.provider.getBalance(deployer);
  console.log(balance);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
```

效果：

```terminal
PS D:\study_test\Hardhat\Harhat-Fundme> yarn hardhat run scripts/fund.js --network hardhat
yarn run v1.22.21
warning package.json: No license field
$ D:\study_test\Hardhat\Harhat-Fundme\node_modules\.bin\hardhat run scripts/fund.js --network hardhat
Deployer address: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
Funding contract...
Funded!
9999999960505000000000n
Done in 5.54s.
```

#### 编写脚本提取资金

P.S 在本地Hardhat环境中运行

```js
//withdraw.js
const { ethers, getNamedAccounts } = require("hardhat");

async function main() {
  const { deployer } = await getNamedAccounts();
  console.log(`Deployer address: ${deployer}`);
  const fundme = await ethers.getContractAt("Fundme", deployer);
  // console.log(`Got contract Fundme at ${fundme.address}`);
  console.log("Funding contract...");
  const transactionResponse = await fundme.withdraw();
  await transactionResponse.wait(1);
  console.log("Got it back!");
  const balance = await ethers.provider.getBalance(deployer);
  console.log(balance);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });

```



## HTML连接到Metamask 

```js
<body>
    that is good
    <button onclick=" connect()">Connect</button>
</body>
<script>
async function connect(){
    if (typeof window.ethereum !=="undefined"){
        await window.ethereum.request({method:"eth_requestAccounts"})
        document.getElementById("connectBUtton").innerHTML="Connected!" //将按钮中文字改为Connected
    }else{
        console.log("No metamask!")
    }
}
</script>
```

也可以

```js
<!-- index.html -->
<body>
    that is good
    <button id ="connectButton" onclick=" connect()">Connect</button>
</body>
<script src="./index.js" type="text/javascript"></script>
```

```js
// index.js
async function connect() {
    if (typeof window.ethereum !== "undefined") {
        await window.ethereum.request({ method: "eth_requestAccounts" })
        document.getElementById("connectButton").innerHTML = "Connected!"
    } else {
        console.log("No metamask!")
    }
}
```

## HTML结合js实现web端交易

[使用Ethers.js代码库发送交易和部署合约 | Moonbeam Docs](https://docs.moonbeam.network/cn/builders/build/eth-api/libraries/ethersjs/)
