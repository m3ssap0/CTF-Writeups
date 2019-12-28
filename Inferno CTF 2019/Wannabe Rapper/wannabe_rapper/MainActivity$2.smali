 
 .class LMainActivity$2;
 .super Ljava/lang/Object;
 .source "MainActivity.java"
 
 # interfaces
 .implements Landroid/view/View$OnClickListener;
 
 
 # annotations
 .annotation system Ldalvik/annotation/EnclosingMethod;
 value = LMainActivity;->onCreate(Landroid/os/Bundle;)V
 .end annotation
 
 .annotation system Ldalvik/annotation/InnerClass;
 accessFlags = 0x0
 name = null
 .end annotation
 
 
 # instance fields
 .field final synthetic this$0:LMainActivity;
 
 
 # direct methods
 .method constructor <init>(LMainActivity;)V
 .registers 2
 
 .line 88
 iput-object p1, p0, LMainActivity$2;->this$0:LMainActivity;
 
 invoke-direct {p0}, Ljava/lang/Object;-><init>()V
 
 return-void
 .end method
 
 
 # virtual methods
 .method public onClick(Landroid/view/View;)V
 .registers 2
 
 .line 91
 iget-object p1, p0, LMainActivity$2;->this$0:LMainActivity;
 
 invoke-virtual {p1}, LMainActivity;->finish()V
 
 .line 92
 return-void
 .end method
 
