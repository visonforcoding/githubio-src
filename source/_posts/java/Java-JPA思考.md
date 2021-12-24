---
title: Java JPA学习
date: 2020-09-23 16:56:11
tags: Java
---

![](http://img.rc5j.cn/blog20200923170827.png)

JPA即Java Persistence API. 2006年5月11号，JPA 1.0 规范作为 JCP JSR 220 的一部分最终被发布。

在PHP世界当中doctrine、cake ORM 都有JPA的影子。

<!--more-->

## Entity

持久化实体是一个轻量级的 Java 类，其状态通常持久地保存到关系数据库的表中。 这种实体的实例对应于表中的各个行。 实体之间通常有关系，这些关系通过对象/关系元数据表示。 可以在实体类文件中直接使用注释来指定这种关系，也可以在随应用程序分发的单独XML描述文件中指定。

## JPQL

Java持久化查询语言 （JPQL）对存储在关系数据库中的实体进行查询。查询在语法上类似于SQL查询，但是操作的是实体对象而不是直接对数据库表进行操作。

## 动机

在引入EJB 3.0规范之前，许多企业级Java开发人员使用由持久化框架（例如Hibernate）或数据访问对象（DAO）提供的轻量级持久化对象，来代替实体bean（EJB的一种）。 这是因为在以前的EJB规范中，实体bean需要太多复杂的代码和繁重的资源占用，并且由于bean和DAO对象或持久化框架之间的源代码中的互连和依赖性，它们只能在Java EE应用程序服务器中使用。 因此，最初在第三方持久性框架中提供的许多功能都被合并到Java Persistence API中，并且从2006年开始，`像Hibernate（版本3.2）和TopLink Essentials这样的项目已经实现Java Persistence API规范。`

## JPA提供商

JPA是一个开源API，因此Oracle，Redhat，Eclipse等各种企业供应商通过在其中添加JPA持久性风格来提供新产品。 其中一些产品包括:

Hibernate, Eclipselink, Toplink, Spring Data JPA, etc.

JSR定义了标准，众多组织对这个标准进行了实现，这使得开发者几乎可以在不同的实现版本里无缝切换。

## spring-data-jpa

事实上Spring-data-jpa并不是jpa的具体实现或提供商。它只是jpa的一个数据访问抽象.在spring-data-jpa中你可以使用
Hibernate, Eclipse Link, 和其他的JPA provider。

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20211222145130.png)

## 注解 Annotations

通常，Xml文件用于配置特定组件，或映射两种不同规格的组件。 在我们的例子中，我们必须在框架中单独维护xml。 这意味着在编写映射xml文件时，我们需要将POJO类属性与mapping.xml文件中的实体标记进行比较。

这是解决方案:在类定义中，我们可以使用注释编写配置部分。 注释用于类，属性和方法。 注释以“@”符号开头。 在声明类，属性或方法之前声明注释。 JPA的所有注释都在javax.persistence包中定义。

以下是我们的示例中使用的注释列表

注解 描述

|  |  |
| --- | --- |
|@Entity| 此批注指定将类声明为实体或表|
|@Table| 此批注指定声明表名。|
|@Basic | 此批注明确指定非约束字段|
|@Embedded| 此批注指定类或实体的属性，该实体的可嵌入类的值实例。|
|@Id| 此批注指定属性，用于类的标识（表的主键）。|
|@GeneratedValue| 此批注指定了如何初始化标识属性，例如自动，手动或从序列表中获取的值。|
|@Transient | 此批注指定了不持久的属性，即该值永远不会存储到数据库中。|
|@Column |此批注用于指定持久性属性的列或属性。|
|@SequenceGenerator |此批注用于定义@GeneratedValue批注中指定的属性的值。 它创建了一个序列。|
|@TableGenerator| 此批注用于指定@GeneratedValue批注中指定的属性的值生成器。 它创建了一个价值生成表。|
|@AccessType| 此类注释用于设置访问类型。 如果设置@AccessType（FIELD），则会发生字段访问。 如果设置@AccessType（PROPERTY），则将进行Property wise评估。|
|@JoinColumn |此批注用于指定实体关联或实体集合。 这用于多对一和一对多关联。|
|@UniqueConstraint| 此批注用于指定主要或辅助表的字段，唯一约束。|
|@ColumnResult |此批注使用select子句引用SQL查询中的列的名称。|
|@ManyToMany| 此批注用于定义连接表之间的多对多关系。|
|@ManyToOne |此批注用于定义连接表之间的多对一关系。|
|@OneToMany| 此批注用于定义连接表之间的一对多关系。|
|@OneToOne| 此批注用于定义连接表之间的一对一关系。|
|@NamedQueries| 此批注用于指定命名查询的列表。|
|@NamedQuery| 此批注用于使用静态名称指定查询。|

### Transient

> 此批注指定了不持久的属性，即该值永远不会存储到数据库中。

JPA默认所有Entity属性都是数据表Column,如果需要增加其他衍生属性而不需要成为数据表字段，则需要此注解。

```java
    private Integer purchasingPriceFen;
    @Transient
    private String purchasingPrice;
    public String getPurchasingPrice() {
        return String.format("%d", this.purchasingPriceFen / 100);
    }
```

本例中，`purchasingPrice`是`purchasingPriceFen`的格式化表示，方便一些实体属性的格式化输出。

### Table

多为数据库表名与entity类名不一致的情况.

```java
@Entity(name = "dorder")
public class Order extends BaseEntity {

}
```

在实际开发当中,我们都希望代码注释和数据表注释越全越好。那么如何使用JPA定义表的注释呢。`javax.persistence.Table`本身办不到，但是其实现方hibernate的Table注解可以。

```java
import org.hibernate.annotations.Table;
@Table(appliesTo = "dorder", comment = "订单表")
public class Order extends BaseEntity {

}
```

### Column

该注解用于定义字段,对应到数据库表的DDL。该字段我建议多使用columnDefinition定义好字段的数据类型,comment

```java
@Column(columnDefinition = "varchar(25) NOT NULL default '无名' comment '商品名'")
private String name;
```

### Temporal

@Temporal 是属性或方法级别的注解，用于声明属性持久化到数据库时所使用的时间精度。该注解可以应用于任何以下类型的实体类属性：

java.util.Date
java.util.Calendar

```java
@Temporal(TemporalType.TIME)
 private Date tokenExpiredTime;

```

## Entity Relationships

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20211223101826.png)

实体关系，RDBMS与NoSQL最直接的区别,直接影响到了我们应用程序的业务数据建模。那么JPA是如何来表示实体关系呢。

### 一对一

关系A和关系B是一对一的关系，一般在一个表里有另一个表的关联id,进行关联。

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20211223102537.png)

例如,用户与当前家庭住址是一对一关系。商品与商品类别是一对一关系。

我们先按官方指导来使用。

```java
//定义地址实体
@Entity
@Table(appliesTo = "address", comment = "地址表")
public class Address extends BaseEntity {
    @Column(columnDefinition = "varchar(50) NOT NULL COMMENT '详细地址'")
    private String detail;

    public String getDetail() {
        return detail;
    }

    public void setDetail(String detail) {
        this.detail = detail;
    }
}
```

```java
//定义用户实体
@Entity
public class User extends BaseEntity {

    @NotBlank(message = "名字不可为空")
    private String name;

    private short age;

    private String mobile;
    
    @OneToOne
    @JoinColumn(name = "address_id", referencedColumnName = "id")
    private Address address;
}
```

`JoinColumn`注解定义了User表的关联字段和关联表address的关联字段。对应到数据库里会自动生成外键并行成外键约束。

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20211223135649.png)

再来看看当表被关联了如何做CURD。

```java
@RestController
@Log4j2
public class UserController {

    @Autowired
    UserService userService;

    @Autowired
    private UserRepository userRepository;

    @PostMapping(name = "用户添加", path = "/user/add")
    public Response add(@Valid @RequestBody User user) {
        Optional<User> user1 = userRepository.findByName(user.getName());
        userRepository.save(user);
        return new Response(0, "获取成功", user);
    }

    @GetMapping(name = "用户详情",path = "/user/{id}")
    public Response detail(@PathVariable Long id){
        Optional<User> user = userRepository.findById(id);
        if (user.isPresent()) {
            return new Response(ResponseCode.success, "获取成功", user.get());
        }
        return new Response(ResponseCode.noDataFound, "获取失败");
    }

}
```

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20211223135833.png)

在数据提交时，关联表的数据用嵌套的json进行提交即可。数据查询时使用`Repository`会自动进行关联查询,查看日志可以看到实际的sql.

```sql
SELECT
    user0_.id AS id1_4_0_,
    user0_.create_time AS create_t2_4_0_,
    user0_.modify_time AS modify_t3_4_0_,
    user0_.address_id AS address_7_4_0_,
    user0_.age AS age4_4_0_,
    user0_.mobile AS mobile5_4_0_,
    user0_.name AS name6_4_0_,
    address1_.id AS id1_0_1_,
    address1_.create_time AS create_t2_0_1_,
    address1_.modify_time AS modify_t3_0_1_,
    address1_.detail AS detail4_0_1_
FROM
    USER user0_
    LEFT OUTER JOIN address address1_ ON user0_.address_id = address1_.id
WHERE
    user0_.id = 3
```

**这点在某种程度上会让开发变得很方便，但也会有潜在的性能风险，因为多表关联数据量大的情况下必然会使得性能下降**

查询结果也以嵌套json对象的形式展现这点非常棒。

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20211223140828.png)

### javax.persistence.CascadeType

在定义关联关系时可以定义,级联的关系操作。

|类型| 说明| 解释
| --- | --- | --- |
|ALL |级联所有实体状态转换 |拥有所有级联操作权限。
|PERSIST |级联实体持久化操作 |当父实体被持久化时，会连同持久化子实体
|MERGE |级联实体合并操作| 当Student中的数据改变，会相应地更新Course中的数据。
|REMOVE |级联实体删除操作| 删除当前实体时，与它有映射关系的实体也会跟着被删除。
|REFRESH |级联实体刷新操作| 假设场景 有一个订单,订单里面关联了许多商品,这个订单可以被很多人操作,那么这个时候A对此订单和关联的商品进行了修改,与此同时,B也进行了相同的操作,但是B先一步比A保存了数据,那么当A保存数据的时候,就需要先刷新订单信息及关联的商品信息后,再将订单及商品保存。
|DETACH |级联实体分离操作|

### FetchType

在定义实体关系的`OneToOne`或其他关系注解时，我们可以定义fetch属性。

- FetchType.LAZY
- FetchType.EAGER

lazy即懒惰模式eager渴望模式。表现差异在于eager会一开始就查找出关联实体，而lazy模式是当你调用相应关联get方法时才会查询。本质区别在于lazy是分sql查询,eager是join关联查询。

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20211223144919.png)

当我们定义`@OneToOne(fetch = FetchType.LAZY)`查看日志的话，我们可以看到之前的join变成了2个select。

不过会存在一个问题是在被指定为lazy的属性对象里返回的json会有个`hibernateLazyInitializer`,如果你不想展示的话可以使用注解`JsonIgnoreProperties`定义到该对象类

```java
@JsonIgnoreProperties(value={"hibernateLazyInitializer"})
public class Address extends BaseEntity {
}
```

### 思考

当在大型应用当中,我建议不要进行外键约束和不要使用EAGER。因为关联查询往往会导致慢查询而拖垮数据库，而1次的sql和2-3次的sql其实在接口层面差异并不明显。

## ManyToMany

在许多场景当中，关系都是多对多的对应关系。拿电商业务来说，订单与商品的关系是多对多的关系。即1个订单可以有多个商品，1个商品可以在多个订单当中。

```java
@Entity(name = "dorder")
@Table(appliesTo = "dorder", comment = "订单表")
public class Order extends BaseEntity {

    private String orderNo;

    private Long uid;

    private Integer status;

    private Integer orderPriceFen;

    @ManyToMany(fetch = FetchType.LAZY)
    @JoinTable(foreignKey = @ForeignKey(value = ConstraintMode.NO_CONSTRAINT),
            inverseForeignKey = @ForeignKey(value = ConstraintMode.NO_CONSTRAINT))
    private Set<Goods> goods;
}
```

- 我们在订单表中定义了goods属性并用`ManyToMany`表示是多对多的关系。
- 使用`ConstraintMode.NO_CONSTRAINT`去除外键约束。
- jpa会生成关联表

```java

    @RequestMapping(path = "/order/create", name = "订单创建", method = RequestMethod.POST)
    public Response createOrder(@Valid @RequestBody Order order) {
        order.setOrderNo(String.format("%d", new Date().getTime()));
        order.setUid(3L);
        Set<Goods> orderGoods = new HashSet<>();
        for (Goods g : order.getGoods()) {
            Optional<Goods> goods = goodsRepository.findById(g.getId());
            goods.ifPresent(orderGoods::add);
        }
        order.setGoods(orderGoods);
        orderRepository.save(order);
        return new Response(ResponseCode.success, "创建成功", order);
    }
```

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20211223190914.png)

### Many-to-Many With a New Entity

有种场景是多对多的关联表还需要其他属性，可能这是实际当中更为常见的情况。比如订单商品表还需要记录商品数量,这个时候最好的方式是用一个新的Entity来建立多对多的关联关系。

```java
@Entity
public class OrderGoods extends BaseEntity {

    @Column(columnDefinition = "int NOT NULL comment '数量'")
    private int nums;

    @ManyToOne
    @JoinColumn(foreignKey = @ForeignKey(value = ConstraintMode.NO_CONSTRAINT))
    @JsonIgnoreProperties(value = {"orderGoods"})
    private Order order;

    @ManyToOne
    @JoinColumn(foreignKey = @ForeignKey(value = ConstraintMode.NO_CONSTRAINT))
    private Goods goods;
}
```

还需对`Goods`和`Order`进行`mappedBy`,防止被重复关联。

```java
@Entity
@Table(appliesTo = "goods", comment = "商品表")
public class Goods extends BaseEntity {
   @OneToMany(mappedBy = "goods")
    private Set<OrderGoods> orderGoods;
}

@Entity(name = "dorder")
@Table(appliesTo = "dorder", comment = "订单表")
public class Order extends BaseEntity {
    @OneToMany(mappedBy = "order")
    @Transient
    @JsonIgnoreProperties(value = {"order"})
    private Set<OrderGoods> orderGoods;
}
```

最终完成订单和订单商品的添加

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20211223232404.png)

### 问题

以上代码与直接的`ManyToMany`方式不同的是，我没能实现主表的save让JPA自动将关联表数据也插入,是我手动处理的。
因为遇到的问题现在还没解决。

想让其自动将关联数据save,把hibernate的info日志打开。会发现`Collection found: was: [<unreferenced>] (initialized)`日志记录,应该是哪里不对，但是目前不纠结了。

以上代码虽然能完成需求但是数据插入并不是在一个事务内执行的，因此实际生产当中这种写法也不可取,需写在一个事务内。

## 参考

1. [https://fanlychie.github.io/post/jpa-column-annotation.html](https://fanlychie.github.io/post/jpa-column-annotation.html)
2. [https://dzone.com/articles/what-is-the-difference-between-hibernate-and-sprin-1](https://dzone.com/articles/what-is-the-difference-between-hibernate-and-sprin-1)
