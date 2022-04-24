---
title: 摘阿里Java开发手册聊聊PHP的ORM框架
date: 2022-04-24 09:55:33
tags:
---
> 任何事情都要有行为准则,否则按照个人直觉做事必定酿成祸端

阿里有一本小册叫做<<阿里JAVA开发手册>>,我们来看看其中关于数据库规范的几条。

1. 超过三个表禁止 join。需要 join 的字段，数据类型保持绝对一致；多表关联查询时，保证被关联的字段需要有索引。
2. 禁止使用存储过程，存储过程难以调试和扩展，更没有移植性。
3. SQL 语句中表的别名前加 as，并且以 t1、t2、t3、...的顺序依次命名。
4. in 操作能避免则避免，若实在避免不了，需要仔细评估 in 后边的集合元素数量，控制在1000 个之内。
5. 表必备三字段：id，create_time，update_time。
6. 在数据库中不能使用物理删除操作，要使用逻辑删除。
7. 不得使用外键与级联，一切外键概念必须在应用层解决。

这几条是我想单独拿出来说的，本文主要讲ORM框架，因此我只说1和7.

<!--more-->

以此为理念我们应当*不使用外键*和*少使用join,甚至默认走多次查询来避免join*。为此我们来看看PHP生态的ORM框架哪种比较适合使用。
我这里对比了ORM框架。

- Laravel Eloquent
- CakePHP ORM
- Cycle ORM
- Doctrine
- Atlas.Orm
更多ORM框架可从[awesome-php](https://github.com/ziadoz/awesome-php#database) 找到。

## Laravel Eloquent

`Laravel`可能是PHP生态最流行的框架了，但是我本人认为Laravel设计的非常差。简单举几个例子：

- route必须逐个在配置文件定义，非常麻烦。不能用注解在控制器方法上定义。
- `lumen`的路由必须带`/api`这样的前缀,很扯。

```php
$users = DB::table('users')
                ->where('votes', '<>', 100)
                ->get();

$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
 
 ```

 这样的查询API不简洁,二维数组的形式很容易出错。并且本质上，
 `Laravel Eloquent`是`ActiveRecord`，并没有`DataMapper`。还不太好说它是ORM.

 更多的对Laravel Eloquent的对比可以在[Add article with comparison to other ORMs](https://github.com/cycle/docs/issues/3) 里找的到。

## Cycle ORM

前面提到的[Add article with comparison to other ORMs](https://github.com/cycle/docs/issues/3)这篇文章,对比了doctrine、Cycle ORM和Eloquent。看起来它比另外两个都要优秀。而且它的官网看起来确实很舒服,看起来很有想做好它的意图。我个人还是比较期待和看好。但是我初步测试了下,Cycle还是要求php8+,鉴于PHP8还没普及应用在PRD我还是直接略过了。

## Doctrine

`Doctrine`是我一度很喜欢的框架,因为它是真正意义上的ORM。并且很多特性与Java JPA很接近，包括`doctrine/annotations`对PHP生态的影响非常深远。

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20220424105819.png)

许多知名框架都有在使用。

`doctrine/annotations`使得很多配置的定义变得很简单，阅读很方便。

并且doctrine的增、删、改的`ActiveRecord` API也设计的非常舒服。

```php
$newProductName = $argv[1];

$product = new Product();
$product->setName($newProductName);

$entityManager->persist($product);
$entityManager->flush();

echo "Created Product with ID " . $product->getId() . "\n";

```

但是在查询这块，尤其你想获得关联关系的嵌套数据结构上会变得很复杂。

```php
<?php
// $em is the EntityManager
$marketId = 1;
$symbol = "AAPL";

$market = $em->find("Doctrine\Tests\Models\StockExchange\Market", $marketId);

// Access the stocks by symbol now:
$stock = $market->getStock($symbol);

echo $stock->getSymbol(); // will print "AAPL"
```

它可以做到关联表的数据对象嵌套,但是问题在于它需要定义外键。

```php
/**
     * @OneToMany(targetEntity="Stock", mappedBy="market", indexBy="symbol")
     * @var Stock[]
     */
    private $stocks;
```

这与我们上面说的`不使用外键`原则相悖。

## CakePHP ORM

`cakephp`是我认为在`ActiveRecord`API中做的最好的一个框架。

但是它的ORM方面并没有doctrine那么吸引人。另一个我不想使用的原因是，它查询出的对象entity,并不是`POJO`或者说`POPO`。

```java
public class MyBean {

    private String someProperty;

    public String getSomeProperty() {
         return someProperty;
    }

    public void setSomeProperty(String someProperty) {
        this.someProperty = someProperty;
    }
}
```

你不能很好的利用IDE来获取对象的属性定义或使用`getter`方法获取。你还是需要打开你的mysql客户端GUI程序来查看表的字段定义。这在编程的时候真的很不方便，很不酷。

## Atlas.Orm

`Atlas.Orm`非常不知名,并且官网很破败,甚至logo图都裂开了。
但是它比较好的一点是，在关联表嵌套数据结构方面足够简单也不需要依赖外键。

```php
class UserRelationships extends MapperRelationships
{
    protected function define()
    {
        $this->oneToMany('addresses',Address::class,[
            'id'=>'user_id'
        ]);
    }
}
```

```php
$users = $this->atlas->select(\App\Model\User\User::class)->with(['addresses'])->where('id > ',0)
->andWhere('age > ',1)
->fetchRecordSet();
```

通过简单的定义和`with`方法就能得到想要的数据结构。并且走的不是join查询,正和我意。

但是,但是！

从它官网的[Contra-Indications](!https://atlasphp.io/)也能看到。

>Atlas uses base Row, Record, and RecordSet classes, instead of plain-old PHP objects. If this were a domain modeling system, a base class would be unacceptable. Because Atlas is a persistence modeling system, base classes are less objectionable, but for some this may be undesired.

它与cakephp一样，也没有POPO,也一样比较难受。虽然它的`Record`有通过`@property`定义字段,还是能是IDE提示属性走起来。但是它所有的返回字段的类型都是string,也没办法通过`getter`进行格式化处理。需要在查询之后遍历处理，这是比较麻烦的重复性工作。

## Atlas.Orm 改造

我强烈希望能使用`doctrine`的ORM特性和`Atlas`的`ActiveRecord`的便利。于是我希望能将两个结合起来,并且希望查询获取到的是POPO对象。

最简单的办法就是将`Atlas`的`fetchRecordSet`结果转化成doctrine的entity popo对象。

这个时候可以使用伟大的`Symfony`的组件`Serializer`。这个组件我经常用来进行array或json到popo的转换,可以想象是Java的Gson类库。

```php
 /**
     * @param $data
     * @return object|array
     */
    public function useObject($data)
    {
        if(is_array($data)){
            return BaseAtlas::ObjectMapper($data,$this->entityClass.'[]');
        }
        return BaseAtlas::ObjectMapper($data,$this->entityClass);

    }


    /**
     * @param mixed $data
     * @param string $mapper
     * @return mixed
     */
    public static function ObjectMapper($data, $mapper)
    {
        $encoders = [new XmlEncoder(), new JsonEncoder()];
        $extractor = new PropertyInfoExtractor([], [new PhpDocExtractor(), new ReflectionExtractor()]);
        $normalizers = [new ObjectNormalizer(null, null, null, $extractor),
            new ArrayDenormalizer(), new JsonSerializableNormalizer()];
        $serializer = new Serializer($normalizers, $encoders);
        return $serializer->deserialize($data, $mapper, 'json', [
            ObjectNormalizer::DISABLE_TYPE_ENFORCEMENT => true]);
    }
```

有两点需要特别注意的是我们需要解决嵌套和数组的映射问题。
`ArrayDenormalizer`和`PhpDocExtractor`需要被用到。
正如网上有的人说的，`Serializer`是一个强大并复杂的组件。要用好它，需要花些时间了解。

## 总结

这样，通过doctrine和atlas的配合使用，CUD使用doctrine，R使用atlas+ObjectMapper。基本解决了我的问题和一直一来坚持的几个原则。

- 80%的工作在处理数据，因此需要一个非常用得习惯的`ActiveRecord`框架。
- 用对象少用PHP Array,把POPO用起来。
- 少使用join
- 不使用外键
