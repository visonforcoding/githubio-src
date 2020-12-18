---
title: Java JPA思考
date: 2020-09-23 16:56:11
tags: Java
---

![](http://img.rc5j.cn/blog20200923170827.png)

JPA即Java Persistence API. 2006年5月11号，JPA 1.0 规范作为 JCP JSR 220 的一部分最终被发布。

在PHP世界当中doctrine、cake ORM 都有JPA的影子。

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

## 注解 Annotations

通常，Xml文件用于配置特定组件，或映射两种不同规格的组件。 在我们的例子中，我们必须在框架中单独维护xml。 这意味着在编写映射xml文件时，我们需要将POJO类属性与mapping.xml文件中的实体标记进行比较。

这是解决方案:在类定义中，我们可以使用注释编写配置部分。 注释用于类，属性和方法。 注释以“@”符号开头。 在声明类，属性或方法之前声明注释。 JPA的所有注释都在javax.persistence包中定义。

以下是我们的示例中使用的注释列表

注解	描述

|  |  |
| --- | --- |
|@Entity|	此批注指定将类声明为实体或表|
|@Table|	此批注指定声明表名。|
|@Basic |	此批注明确指定非约束字段|
|@Embedded|	此批注指定类或实体的属性，该实体的可嵌入类的值实例。|
|@Id|	此批注指定属性，用于类的标识（表的主键）。|
|@GeneratedValue|	此批注指定了如何初始化标识属性，例如自动，手动或从序列表中获取的值。|
|@Transient |	此批注指定了不持久的属性，即该值永远不会存储到数据库中。|
|@Column	|此批注用于指定持久性属性的列或属性。|
|@SequenceGenerator	|此批注用于定义@GeneratedValue批注中指定的属性的值。 它创建了一个序列。|
|@TableGenerator|	此批注用于指定@GeneratedValue批注中指定的属性的值生成器。 它创建了一个价值生成表。|
|@AccessType|	此类注释用于设置访问类型。 如果设置@AccessType（FIELD），则会发生字段访问。 如果设置@AccessType（PROPERTY），则将进行Property wise评估。|
|@JoinColumn	|此批注用于指定实体关联或实体集合。 这用于多对一和一对多关联。|
|@UniqueConstraint|	此批注用于指定主要或辅助表的字段，唯一约束。|
|@ColumnResult	|此批注使用select子句引用SQL查询中的列的名称。|
|@ManyToMany|	此批注用于定义连接表之间的多对多关系。|
|@ManyToOne	|此批注用于定义连接表之间的多对一关系。|
|@OneToMany|	此批注用于定义连接表之间的一对多关系。|
|@OneToOne|	此批注用于定义连接表之间的一对一关系。|
|@NamedQueries|	此批注用于指定命名查询的列表。|
|@NamedQuery|	此批注用于使用静态名称指定查询。|



